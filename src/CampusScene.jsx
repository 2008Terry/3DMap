import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { CSS2DObject, CSS2DRenderer } from 'three/addons/renderers/CSS2DRenderer.js';

const INITIAL_CAMERA = new THREE.Vector3(390, 475, 570);
const INITIAL_TARGET = new THREE.Vector3(0, 0, 0);
const LABEL_NAMES = {
  'hatcher-graduate-library': 'Hatcher Library',
  'shapiro-undergraduate-library': 'Shapiro Library',
  'burton-memorial-tower': 'Burton Tower',
  'rackham-building': 'Rackham',
};

function polygonShape(ring) {
  // Three's shape plane is X/Y; after rotation its Y axis becomes north (-Z).
  const shape = new THREE.Shape();
  ring.forEach(([x, z], index) => {
    if (index === 0) shape.moveTo(x, -z);
    else shape.lineTo(x, -z);
  });
  shape.closePath();
  return shape;
}

function surface(ring, color, y) {
  const mesh = new THREE.Mesh(
    new THREE.ShapeGeometry(polygonShape(ring)),
    new THREE.MeshStandardMaterial({ color, roughness: 1, side: THREE.DoubleSide }),
  );
  mesh.rotation.x = -Math.PI / 2;
  mesh.position.y = y;
  mesh.receiveShadow = true;
  return mesh;
}

function buildingMesh(building, part) {
  const material = new THREE.MeshStandardMaterial({
    color: building.color,
    roughness: 0.83,
    metalness: 0.04,
  });
  const mesh = new THREE.Mesh(
    new THREE.ExtrudeGeometry(polygonShape(part.footprint), {
      depth: part.heightMeters,
      bevelEnabled: false,
      steps: 1,
    }),
    material,
  );
  mesh.rotation.x = -Math.PI / 2;
  mesh.position.y = 0.18;
  mesh.castShadow = true;
  mesh.receiveShadow = true;
  mesh.userData.buildingId = building.id;
  mesh.userData.baseColor = material.color.clone();
  return mesh;
}

function southFacadeDetails(building, part) {
  const details = building.facadeDetails;
  if (!details) return [];

  const ring = part.footprint;
  const edges = ring.slice(0, -1).map((point, index) => {
    const next = ring[index + 1];
    const dx = next[0] - point[0];
    const dz = next[1] - point[1];
    return { point, next, dx, dz, length: Math.hypot(dx, dz), midSouth: (point[1] + next[1]) / 2 };
  }).filter((edge) => Math.abs(edge.dx) > Math.abs(edge.dz) * 2);
  const facade = edges.sort((a, b) => b.midSouth - a.midSouth)[0];
  if (!facade) return [];

  const baseY = 0.18;
  const height = part.heightMeters * 0.44;
  const radius = facade.length * 0.018;
  const bodyHeight = height * 0.88;
  const normalX = -facade.dz / facade.length;
  const normalZ = facade.dx / facade.length;
  const material = new THREE.MeshStandardMaterial({ color: '#c5bda8', roughness: 0.86 });
  const meshes = [];
  const addCylinder = (x, z, y, cylinderHeight, bottomRadius, topRadius) => {
    const mesh = new THREE.Mesh(
      new THREE.CylinderGeometry(topRadius, bottomRadius, cylinderHeight, 12),
      material,
    );
    mesh.position.set(x, y, z);
    mesh.castShadow = true;
    mesh.receiveShadow = true;
    mesh.userData.buildingId = building.id;
    mesh.userData.baseColor = material.color.clone();
    meshes.push(mesh);
  };

  const anchors = [];
  const count = details.southPorticoColumns || 0;
  for (let index = 0; index < count; index += 1) {
    const progress = 0.12 + (0.76 * index) / (count - 1);
    const x = facade.point[0] + facade.dx * progress + normalX * radius * 0.2;
    const z = facade.point[1] + facade.dz * progress + normalZ * radius * 0.2;
    anchors.push([x, z]);
    addCylinder(x, z, baseY + bodyHeight / 2, bodyHeight, radius * 0.72, radius * 0.58);
    addCylinder(x, z, baseY + bodyHeight + 0.12, 0.24, radius * 0.9, radius * 0.9);
    addCylinder(x, z, baseY + height - 0.18, 0.36, radius * 0.95, radius * 0.95);
  }

  const midpointX = (facade.point[0] + facade.next[0]) / 2 + normalX * radius * 0.2;
  const midpointZ = (facade.point[1] + facade.next[1]) / 2 + normalZ * radius * 0.2;
  if (count) {
    const beam = new THREE.Mesh(
      new THREE.BoxGeometry(facade.length * 0.82, 0.62, radius * 1.8),
      material,
    );
    beam.position.set(midpointX, baseY + height + 0.14, midpointZ);
    beam.rotation.y = -Math.atan2(facade.dz, facade.dx);
    beam.castShadow = true;
    beam.receiveShadow = true;
    beam.userData.buildingId = building.id;
    beam.userData.baseColor = material.color.clone();
    meshes.push(beam);
  }

  details.southStringcourses?.forEach((fraction, index) => {
    const course = new THREE.Mesh(
      new THREE.BoxGeometry(facade.length, 0.24, radius * 0.8),
      new THREE.MeshStandardMaterial({ color: index === 0 ? '#d2cbbc' : '#a87560', roughness: 0.9 }),
    );
    course.position.set(midpointX, baseY + part.heightMeters * fraction, midpointZ);
    course.rotation.y = -Math.atan2(facade.dz, facade.dx);
    course.castShadow = true;
    course.receiveShadow = true;
    course.userData.buildingId = building.id;
    course.userData.baseColor = course.material.color.clone();
    meshes.push(course);
  });
  return meshes;
}

function buildingCenter(rings) {
  const points = rings.flatMap((ring) => ring.slice(0, -1));
  const [x, z] = points.reduce(([sumX, sumZ], point) => [sumX + point[0], sumZ + point[1]], [0, 0]);
  return [x / points.length, z / points.length];
}

export default function CampusScene({
  buildings,
  context,
  selectedBuildingId,
  resetCameraKey,
  onBuildingSelect,
  onClearSelection,
}) {
  const mountRef = useRef(null);
  const sceneStateRef = useRef(null);
  const selectRef = useRef(onBuildingSelect);
  const clearRef = useRef(onClearSelection);

  useEffect(() => { selectRef.current = onBuildingSelect; }, [onBuildingSelect]);
  useEffect(() => { clearRef.current = onClearSelection; }, [onClearSelection]);

  useEffect(() => {
    const mount = mountRef.current;
    if (!mount) return undefined;

    const scene = new THREE.Scene();
    scene.background = new THREE.Color('#dbe8e3');
    scene.fog = new THREE.Fog('#dbe8e3', 850, 1500);

    const camera = new THREE.PerspectiveCamera(46, 1, 1, 2200);
    camera.position.copy(INITIAL_CAMERA);
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    renderer.domElement.className = 'campus-canvas';
    renderer.domElement.setAttribute('aria-label', 'Interactive three-dimensional map centered on the University of Michigan Diag');
    mount.appendChild(renderer.domElement);

    const labelRenderer = new CSS2DRenderer();
    labelRenderer.domElement.className = 'campus-label-layer';
    mount.appendChild(labelRenderer.domElement);

    const controls = new OrbitControls(camera, renderer.domElement);
    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
    controls.enableDamping = !reduceMotion.matches;
    controls.dampingFactor = 0.08;
    controls.minDistance = 135;
    controls.maxDistance = 1250;
    controls.maxPolarAngle = Math.PI * 0.47;
    controls.target.copy(INITIAL_TARGET);
    controls.update();
    const buildingLabels = new Map();
    sceneStateRef.current = {
      camera,
      controls,
      buildingMeshes: new Map(),
      buildingLabels,
      buildingFocus: new Map(),
      selectedBuildingId: null,
    };

    scene.add(new THREE.HemisphereLight('#ffffff', '#758f84', 2.4));
    const sunlight = new THREE.DirectionalLight('#fff8e9', 2.25);
    sunlight.position.set(-270, 480, 210);
    sunlight.castShadow = true;
    sunlight.shadow.mapSize.set(2048, 2048);
    sunlight.shadow.camera.left = -510;
    sunlight.shadow.camera.right = 510;
    sunlight.shadow.camera.top = 510;
    sunlight.shadow.camera.bottom = -510;
    sunlight.shadow.camera.near = 1;
    sunlight.shadow.camera.far = 1100;
    sunlight.shadow.bias = -0.0003;
    scene.add(sunlight);

    const ground = new THREE.Mesh(
      new THREE.PlaneGeometry(860, 860),
      new THREE.MeshStandardMaterial({ color: '#a5bdb0', roughness: 1 }),
    );
    ground.rotation.x = -Math.PI / 2;
    ground.receiveShadow = true;
    scene.add(ground);

    context.streets.forEach(({ footprint }) => scene.add(surface(footprint, '#b8c4bc', 0.025)));
    const lawn = surface(context.diagLawn, '#8eaa8d', 0.055);
    scene.add(lawn);
    context.paths.forEach(({ footprint }) => scene.add(surface(footprint, '#d9d6c8', 0.09)));

    const buildingMeshes = [];
    let suppressLabelClick = false;
    const onLabelClick = (event) => {
      // Native button activation also provides Enter/Space keyboard selection.
      if (event.detail === 0 || !suppressLabelClick) {
        selectRef.current(event.currentTarget.dataset.buildingId);
      }
    };
    buildings.forEach((building) => {
      const meshes = building.parts.flatMap((part) => {
        const mesh = buildingMesh(building, part);
        scene.add(mesh);
        buildingMeshes.push(mesh);
        const details = southFacadeDetails(building, part);
        details.forEach((detail) => {
          scene.add(detail);
          buildingMeshes.push(detail);
        });
        return [mesh, ...details];
      });
      sceneStateRef.current.buildingMeshes.set(building.id, meshes);
      const rings = building.parts.map((part) => part.footprint);
      const [centerX, centerZ] = buildingCenter(rings);
      const points = rings.flatMap((ring) => ring.slice(0, -1));
      const width = Math.max(...points.map(([x]) => x)) - Math.min(...points.map(([x]) => x));
      const depth = Math.max(...points.map(([, z]) => z)) - Math.min(...points.map(([, z]) => z));
      sceneStateRef.current.buildingFocus.set(building.id, {
        centerX,
        centerZ,
        height: building.heightMeters,
        distance: Math.max(125, Math.max(width, depth) * 1.8, building.heightMeters * 2.2),
      });

      const labelElement = document.createElement('button');
      labelElement.type = 'button';
      labelElement.className = 'campus-building-label';
      labelElement.textContent = LABEL_NAMES[building.id] || building.name;
      labelElement.title = building.name;
      labelElement.setAttribute('aria-label', `Select ${building.name}`);
      labelElement.setAttribute('aria-pressed', 'false');
      labelElement.dataset.buildingId = building.id;
      labelElement.addEventListener('click', onLabelClick);
      const label = new CSS2DObject(labelElement);
      const [x, z] = buildingCenter(building.parts.map((part) => part.footprint));
      label.position.set(x, building.heightMeters + 3, z);
      label.userData.buildingId = building.id;
      scene.add(label);
      buildingLabels.set(building.id, label);
    });

    const raycaster = new THREE.Raycaster();
    const pointer = new THREE.Vector2();
    const activePointers = new Map();
    let multiPointerGesture = false;
    const onPointerDown = (event) => {
      if (activePointers.size === 0) suppressLabelClick = false;
      activePointers.set(event.pointerId, {
        x: event.clientX,
        y: event.clientY,
        dragged: false,
        canvas: event.target === renderer.domElement,
        primaryButton: event.button === 0,
      });
      if (activePointers.size > 1) {
        multiPointerGesture = true;
        suppressLabelClick = true;
      }
    };
    const onPointerMove = (event) => {
      const pointerDown = activePointers.get(event.pointerId);
      if (!pointerDown) return;
      if (Math.hypot(event.clientX - pointerDown.x, event.clientY - pointerDown.y) > 5) {
        pointerDown.dragged = true;
        suppressLabelClick = true;
      }
    };
    const onPointerCancel = (event) => {
      if (!activePointers.delete(event.pointerId)) return;
      suppressLabelClick = true;
      if (activePointers.size === 0) multiPointerGesture = false;
    };
    const onPointerUp = (event) => {
      const pointerDown = activePointers.get(event.pointerId);
      if (!pointerDown) return;
      const moved = pointerDown.dragged
        || Math.hypot(event.clientX - pointerDown.x, event.clientY - pointerDown.y) > 5;
      const suppressed = multiPointerGesture || moved || !pointerDown.primaryButton;
      suppressLabelClick = suppressLabelClick || suppressed;
      activePointers.delete(event.pointerId);
      if (activePointers.size === 0) multiPointerGesture = false;
      if (suppressed || !pointerDown.canvas || event.target !== renderer.domElement) return;

      const bounds = renderer.domElement.getBoundingClientRect();
      if (!bounds.width || !bounds.height) return;
      if (event.clientX < bounds.left || event.clientX > bounds.right
        || event.clientY < bounds.top || event.clientY > bounds.bottom) return;
      pointer.set(
        ((event.clientX - bounds.left) / bounds.width) * 2 - 1,
        -((event.clientY - bounds.top) / bounds.height) * 2 + 1,
      );
      raycaster.setFromCamera(pointer, camera);
      const hit = raycaster.intersectObjects(buildingMeshes, false)[0];
      if (hit) selectRef.current(hit.object.userData.buildingId);
      else if (raycaster.intersectObject(ground, false).length) clearRef.current();
    };
    // Capture starts on both canvas and labels; window listeners follow releases outside the map.
    mount.addEventListener('pointerdown', onPointerDown, true);
    window.addEventListener('pointermove', onPointerMove, true);
    window.addEventListener('pointerup', onPointerUp, true);
    window.addEventListener('pointercancel', onPointerCancel, true);

    const resize = () => {
      const { width, height } = mount.getBoundingClientRect();
      if (!width || !height) return;
      camera.aspect = width / height;
      camera.updateProjectionMatrix();
      renderer.setSize(width, height, false);
      labelRenderer.setSize(width, height);
    };
    const resizeObserver = new ResizeObserver(resize);
    resizeObserver.observe(mount);
    resize();

    let frameId;
    const resolveLabelOverlaps = () => {
      const selectedId = sceneStateRef.current.selectedBuildingId;
      const labels = [...buildingLabels.values()].sort((a, b) => {
        if (a.userData.buildingId === selectedId) return -1;
        if (b.userData.buildingId === selectedId) return 1;
        return 0;
      });
      const visibleBounds = [];
      labels.forEach((label, index) => {
        const element = label.element;
        // CSS2DRenderer sets display for labels outside the camera's depth range.
        element.style.visibility = '';
        element.style.zIndex = String(labels.length - index);
        if (element.style.display === 'none') return;
        const bounds = element.getBoundingClientRect();
        const overlaps = visibleBounds.some((other) => bounds.left < other.right
          && bounds.right > other.left && bounds.top < other.bottom && bounds.bottom > other.top);
        if (overlaps) element.style.visibility = 'hidden';
        else visibleBounds.push(bounds);
      });
    };
    const render = () => {
      frameId = window.requestAnimationFrame(render);
      if (controls.enableDamping) controls.update();
      renderer.render(scene, camera);
      labelRenderer.render(scene, camera);
      resolveLabelOverlaps();
    };
    render();

    return () => {
      window.cancelAnimationFrame(frameId);
      resizeObserver.disconnect();
      mount.removeEventListener('pointerdown', onPointerDown, true);
      window.removeEventListener('pointermove', onPointerMove, true);
      window.removeEventListener('pointerup', onPointerUp, true);
      window.removeEventListener('pointercancel', onPointerCancel, true);
      buildingLabels.forEach((label) => label.element.removeEventListener('click', onLabelClick));
      controls.dispose();
      scene.traverse((object) => {
        object.geometry?.dispose();
        if (Array.isArray(object.material)) object.material.forEach((material) => material.dispose());
        else object.material?.dispose();
        object.shadow?.map?.dispose();
      });
      renderer.dispose();
      mount.removeChild(renderer.domElement);
      mount.removeChild(labelRenderer.domElement);
      sceneStateRef.current = null;
    };
  }, [buildings, context]);

  useEffect(() => {
    const state = sceneStateRef.current;
    if (!state) return;
    state.selectedBuildingId = selectedBuildingId;
    state.buildingMeshes.forEach((meshes, id) => {
      const selected = id === selectedBuildingId;
      meshes.forEach((mesh) => {
        mesh.material.color.set(selected ? '#e8d393' : mesh.userData.baseColor);
        mesh.material.emissive.set(selected ? '#514021' : '#000000');
        mesh.material.emissiveIntensity = selected ? 0.24 : 0;
      });
    });
    state.buildingLabels.forEach((label, id) => {
      const selected = id === selectedBuildingId;
      label.element.classList.toggle('is-selected', selected);
      label.element.setAttribute('aria-pressed', String(selected));
    });
    const focus = state.buildingFocus.get(selectedBuildingId);
    if (focus) {
      const offset = state.camera.position.clone().sub(state.controls.target);
      const target = new THREE.Vector3(focus.centerX, focus.height * 0.34, focus.centerZ);
      offset.setLength(focus.distance);
      state.controls.target.copy(target);
      state.camera.position.copy(target).add(offset);
      state.controls.update();
    }
  }, [selectedBuildingId, buildings, context]);

  useEffect(() => {
    const state = sceneStateRef.current;
    if (!state) return;
    state.controls.target.copy(INITIAL_TARGET);
    state.camera.position.copy(INITIAL_CAMERA);
    state.controls.update();
  }, [resetCameraKey]);

  return <div className="campus-scene" ref={mountRef} />;
}
