import { useEffect, useRef } from 'react';
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

function buildingMesh(building) {
  const material = new THREE.MeshStandardMaterial({
    color: building.category === 'Landmark' ? '#c5cbbd' : '#b7c9c5',
    roughness: 0.83,
    metalness: 0.04,
  });
  const mesh = new THREE.Mesh(
    new THREE.ExtrudeGeometry(polygonShape(building.footprint), {
      depth: building.heightMeters,
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

function buildingCenter(ring) {
  const points = ring.slice(0, -1);
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
    labelRenderer.domElement.setAttribute('aria-hidden', 'true');
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
    sceneStateRef.current = { camera, controls, buildingMeshes: new Map() };

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

    context.streets.forEach(({ footprint }) => scene.add(surface(footprint, '#899997', 0.025)));
    const lawn = surface(context.diagLawn, '#79a47a', 0.055);
    scene.add(lawn);
    context.paths.forEach(({ footprint }) => scene.add(surface(footprint, '#d9d0ba', 0.09)));

    const buildingMeshes = [];
    buildings.forEach((building) => {
      const mesh = buildingMesh(building);
      scene.add(mesh);
      buildingMeshes.push(mesh);
      sceneStateRef.current.buildingMeshes.set(building.id, mesh);

      const labelElement = document.createElement('span');
      labelElement.className = 'campus-building-label';
      labelElement.textContent = LABEL_NAMES[building.id] || building.name;
      labelElement.title = building.name;
      labelElement.dataset.buildingId = building.id;
      const label = new CSS2DObject(labelElement);
      const [x, z] = buildingCenter(building.footprint);
      label.position.set(x, building.heightMeters + 3, z);
      label.userData.buildingId = building.id;
      scene.add(label);
    });

    const raycaster = new THREE.Raycaster();
    const pointer = new THREE.Vector2();
    let pointerDown = null;
    const onPointerDown = (event) => {
      if (event.button !== 0) return;
      pointerDown = { id: event.pointerId, x: event.clientX, y: event.clientY, dragged: false };
    };
    const onPointerMove = (event) => {
      if (!pointerDown || pointerDown.id !== event.pointerId) return;
      if (Math.hypot(event.clientX - pointerDown.x, event.clientY - pointerDown.y) > 5) {
        pointerDown.dragged = true;
      }
    };
    const onPointerCancel = () => { pointerDown = null; };
    const onPointerUp = (event) => {
      if (!pointerDown || pointerDown.id !== event.pointerId) return;
      const moved = pointerDown.dragged
        || Math.hypot(event.clientX - pointerDown.x, event.clientY - pointerDown.y) > 5;
      pointerDown = null;
      if (moved) return;

      const bounds = renderer.domElement.getBoundingClientRect();
      if (!bounds.width || !bounds.height) return;
      pointer.set(
        ((event.clientX - bounds.left) / bounds.width) * 2 - 1,
        -((event.clientY - bounds.top) / bounds.height) * 2 + 1,
      );
      raycaster.setFromCamera(pointer, camera);
      const hit = raycaster.intersectObjects(buildingMeshes, false)[0];
      if (hit) selectRef.current(hit.object.userData.buildingId);
      else if (raycaster.intersectObject(ground, false).length) clearRef.current();
    };
    renderer.domElement.addEventListener('pointerdown', onPointerDown);
    renderer.domElement.addEventListener('pointermove', onPointerMove);
    renderer.domElement.addEventListener('pointerup', onPointerUp);
    renderer.domElement.addEventListener('pointercancel', onPointerCancel);

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
    const render = () => {
      frameId = window.requestAnimationFrame(render);
      if (controls.enableDamping) controls.update();
      renderer.render(scene, camera);
      labelRenderer.render(scene, camera);
    };
    render();

    return () => {
      window.cancelAnimationFrame(frameId);
      resizeObserver.disconnect();
      renderer.domElement.removeEventListener('pointerdown', onPointerDown);
      renderer.domElement.removeEventListener('pointermove', onPointerMove);
      renderer.domElement.removeEventListener('pointerup', onPointerUp);
      renderer.domElement.removeEventListener('pointercancel', onPointerCancel);
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
    state.buildingMeshes.forEach((mesh, id) => {
      const selected = id === selectedBuildingId;
      mesh.material.color.set(selected ? '#e8d393' : mesh.userData.baseColor);
      mesh.material.emissive.set(selected ? '#514021' : '#000000');
      mesh.material.emissiveIntensity = selected ? 0.24 : 0;
    });
    mountRef.current?.querySelectorAll('.campus-building-label').forEach((element) => {
      element.classList.toggle('is-selected', element.dataset.buildingId === selectedBuildingId);
    });
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
