import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { CSS2DObject, CSS2DRenderer } from 'three/addons/renderers/CSS2DRenderer.js';

const FLOOR_HEIGHT = 2.8;
const FLOOR_EXPLODE_GAP = 1;
const FLOOR_COLORS = ['#b5ded8', '#bdd2dd', '#d4c8e7', '#e4d5b9'];

function addBox(parent, size, position, material, name) {
  const mesh = new THREE.Mesh(new THREE.BoxGeometry(...size), material);
  mesh.position.set(...position);
  if (name) mesh.name = name;
  mesh.castShadow = true;
  mesh.receiveShadow = true;
  parent.add(mesh);
  return mesh;
}

function addRoomLabel(parent, room, onRoomSelect) {
  const button = document.createElement('button');
  button.className = 'room-label';
  button.type = 'button';
  button.textContent = room.number;
  button.setAttribute('aria-label', `${room.number} ${room.name}，${room.use}`);
  button.addEventListener('click', (event) => {
    event.stopPropagation();
    onRoomSelect(room.id);
  });
  const label = new CSS2DObject(button);
  label.position.set(room.x, 1.35, room.z);
  label.userData.roomId = room.id;
  parent.add(label);
  return { label, button };
}

function buildFloor(scene, floorId, rooms, onRoomSelect) {
  const floor = new THREE.Group();
  floor.name = `floor-${floorId}`;
  floor.userData.floorId = floorId;
  floor.userData.baseY = (floorId - 1) * FLOOR_HEIGHT;
  floor.userData.targetY = floor.userData.baseY;
  floor.position.y = floor.userData.baseY;

  const baseMaterial = new THREE.MeshStandardMaterial({ color: '#d5e2df', roughness: 0.9 });
  const corridorMaterial = new THREE.MeshStandardMaterial({ color: '#f0f1e9', roughness: 0.85 });
  const wallMaterial = new THREE.MeshStandardMaterial({ color: '#b9ccca', roughness: 0.88 });
  const roomMaterial = new THREE.MeshStandardMaterial({ color: FLOOR_COLORS[floorId - 1], roughness: 0.85 });
  const trimMaterial = new THREE.MeshStandardMaterial({ color: '#78979a', roughness: 0.74 });

  addBox(floor, [10, 0.22, 8.5], [0, 0, 0], baseMaterial, 'floor-slab');
  addBox(floor, [1.25, 0.07, 7.8], [0, 0.145, 0], corridorMaterial, 'corridor');

  for (const room of rooms) {
    const roomMesh = addBox(
      floor,
      [room.width, 0.08, room.depth],
      [room.x, 0.18, room.z],
      roomMaterial.clone(),
      `room-${room.id}`,
    );
    roomMesh.userData.roomId = room.id;
    roomMesh.userData.floorId = floorId;

    const wallHeight = 1.15;
    const wallThickness = 0.1;
    const xEdge = room.width / 2;
    const zEdge = room.depth / 2;
    addBox(floor, [wallThickness, wallHeight, room.depth], [room.x - xEdge, 0.18 + wallHeight / 2, room.z], wallMaterial);
    addBox(floor, [wallThickness, wallHeight, room.depth], [room.x + xEdge, 0.18 + wallHeight / 2, room.z], wallMaterial);
    addBox(floor, [room.width, wallHeight, wallThickness], [room.x, 0.18 + wallHeight / 2, room.z - zEdge], wallMaterial);
    addBox(floor, [room.width, wallHeight, wallThickness], [room.x, 0.18 + wallHeight / 2, room.z + zEdge], wallMaterial);

    addBox(floor, [0.055, 1.35, 0.055], [room.x - xEdge + 0.04, 0.18 + wallHeight + 0.66, room.z - zEdge + 0.04], trimMaterial);
    addRoomLabel(floor, room, onRoomSelect);
  }

  scene.add(floor);
  return floor;
}

export default function BuildingScene({
  rooms,
  selectedFloor,
  selectedRoomId,
  exploded,
  resetCameraKey,
  onRoomSelect,
  onClearSelection,
}) {
  const mountRef = useRef(null);
  const sceneRef = useRef(null);
  const explodedRef = useRef(exploded);
  const roomSelectRef = useRef(onRoomSelect);
  const clearSelectionRef = useRef(onClearSelection);
  const controlsRef = useRef(null);

  useEffect(() => { roomSelectRef.current = onRoomSelect; }, [onRoomSelect]);
  useEffect(() => { clearSelectionRef.current = onClearSelection; }, [onClearSelection]);

  useEffect(() => {
    const mount = mountRef.current;
    if (!mount) return undefined;

    const scene = new THREE.Scene();
    sceneRef.current = scene;
    scene.background = null;
    const camera = new THREE.PerspectiveCamera(34, 1, 0.1, 100);
    const defaultCameraPosition = new THREE.Vector3(14.5, 14, 17);
    const defaultLookAt = new THREE.Vector3(0, 4.3, 0);
    camera.position.copy(defaultCameraPosition);
    camera.lookAt(defaultLookAt);

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.16;
    renderer.domElement.className = 'building-canvas';
    renderer.domElement.setAttribute('aria-label', '四层虚拟建筑 3D 模型，可拖动旋转、滚轮缩放并点击房间');
    renderer.domElement.setAttribute('role', 'img');
    mount.appendChild(renderer.domElement);

    const labelRenderer = new CSS2DRenderer();
    labelRenderer.domElement.className = 'room-label-layer';
    labelRenderer.domElement.setAttribute('aria-label', '房间编号；使用 Tab 键可选择房间');
    mount.appendChild(labelRenderer.domElement);

    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.075;
    controls.minDistance = 11;
    controls.maxDistance = 31;
    controls.maxPolarAngle = Math.PI * 0.49;
    controls.target.copy(defaultLookAt);
    controlsRef.current = { controls, camera, defaultCameraPosition, defaultLookAt };

    scene.add(new THREE.HemisphereLight('#efffff', '#49626a', 2.15));
    const keyLight = new THREE.DirectionalLight('#fff5dc', 3.1);
    keyLight.position.set(9, 18, 10);
    keyLight.castShadow = true;
    keyLight.shadow.mapSize.set(1024, 1024);
    scene.add(keyLight);
    const fillLight = new THREE.DirectionalLight('#8ad8d2', 1.3);
    fillLight.position.set(-10, 9, -7);
    scene.add(fillLight);

    const floors = new Map();
    for (let floorId = 1; floorId <= 4; floorId += 1) {
      const floorRooms = rooms.filter((room) => room.floor === floorId);
      const floor = buildFloor(scene, floorId, floorRooms, (roomId) => roomSelectRef.current(roomId));
      floors.set(floorId, floor);
    }

    const raycaster = new THREE.Raycaster();
    const pointer = new THREE.Vector2();
    const downPoint = new THREE.Vector2();
    let pointerDown = false;
    const onPointerDown = (event) => {
      downPoint.set(event.clientX, event.clientY);
      pointerDown = true;
    };
    const onPointerUp = (event) => {
      if (!pointerDown) return;
      pointerDown = false;
      if (Math.hypot(event.clientX - downPoint.x, event.clientY - downPoint.y) > 5) return;
      const bounds = renderer.domElement.getBoundingClientRect();
      pointer.set(
        ((event.clientX - bounds.left) / bounds.width) * 2 - 1,
        -((event.clientY - bounds.top) / bounds.height) * 2 + 1,
      );
      raycaster.setFromCamera(pointer, camera);
      const roomMeshes = [];
      floors.forEach((floor) => floor.traverse((object) => {
        if (object.isMesh && object.userData.roomId) roomMeshes.push(object);
      }));
      const hit = raycaster.intersectObjects(roomMeshes, false)[0];
      if (hit) roomSelectRef.current(hit.object.userData.roomId);
      else clearSelectionRef.current();
    };
    renderer.domElement.addEventListener('pointerdown', onPointerDown);
    renderer.domElement.addEventListener('pointerup', onPointerUp);

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

    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
    let frameId = 0;
    const render = () => {
      frameId = window.requestAnimationFrame(render);
      const dt = Math.min(clock.getDelta(), 0.05);
      floors.forEach((floor) => {
        const { targetY } = floor.userData;
        if (reduceMotion.matches) floor.position.y = targetY;
        else floor.position.y = THREE.MathUtils.damp(floor.position.y, targetY, 6, dt);
      });
      controls.update();
      renderer.render(scene, camera);
      labelRenderer.render(scene, camera);
    };
    const clock = new THREE.Clock();
    render();

    return () => {
      window.cancelAnimationFrame(frameId);
      resizeObserver.disconnect();
      renderer.domElement.removeEventListener('pointerdown', onPointerDown);
      renderer.domElement.removeEventListener('pointerup', onPointerUp);
      controls.dispose();
      floors.forEach((floor) => {
        floor.traverse((object) => {
          if (object.isMesh) {
            object.geometry.dispose();
            if (Array.isArray(object.material)) object.material.forEach((material) => material.dispose());
            else object.material.dispose();
          }
        });
        scene.remove(floor);
      });
      scene.traverse((object) => {
        if (object.isLight && object.shadow?.map) object.shadow.map.dispose();
      });
      renderer.dispose();
      mount.removeChild(renderer.domElement);
      mount.removeChild(labelRenderer.domElement);
      controlsRef.current = null;
      sceneRef.current = null;
    };
  }, [rooms]);

  useEffect(() => {
    floorsUpdate(sceneRef.current, exploded, selectedFloor, selectedRoomId);
  }, [exploded, selectedFloor, selectedRoomId]);

  useEffect(() => {
    explodedRef.current = exploded;
    const state = controlsRef.current;
    if (!state) return;
    const zoom = exploded ? 1.2 : 1 / 1.2;
    const viewDirection = state.camera.position.clone().sub(state.controls.target).multiplyScalar(zoom);
    const target = state.controls.target.clone();
    target.y = state.defaultLookAt.y + (exploded ? FLOOR_EXPLODE_GAP * 1.5 : 0);
    state.controls.target.copy(target);
    state.camera.position.copy(target).add(viewDirection);
    state.controls.update();
  }, [exploded]);

  useEffect(() => {
    const state = controlsRef.current;
    if (!state) return;
    const zoom = explodedRef.current ? 1.2 : 1;
    const target = state.defaultLookAt.clone();
    target.y += explodedRef.current ? FLOOR_EXPLODE_GAP * 1.5 : 0;
    const viewDirection = state.defaultCameraPosition.clone().sub(state.defaultLookAt).multiplyScalar(zoom);
    state.controls.target.copy(target);
    state.camera.position.copy(target).add(viewDirection);
    state.controls.update();
  }, [resetCameraKey]);

  return <div className="building-scene" ref={mountRef} />;
}

function floorsUpdate(scene, exploded, selectedFloor, selectedRoomId) {
  if (!scene) return;
  scene.traverse((object) => {
    if (!object.isGroup || !object.userData.floorId) return;
    const floorId = object.userData.floorId;
    const offset = exploded ? (floorId - 1) * FLOOR_EXPLODE_GAP : 0;
    object.userData.targetY = object.userData.baseY + offset;
    const dim = selectedFloor !== null && floorId !== selectedFloor;
    object.traverse((child) => {
      if (child.isMesh) {
        const isSelectedRoom = child.userData.roomId === selectedRoomId;
        const shouldDim = dim && !isSelectedRoom;
        const materials = Array.isArray(child.material) ? child.material : [child.material];
        materials.forEach((material) => {
          if (material.transparent !== shouldDim) {
            material.transparent = shouldDim;
            material.needsUpdate = true;
          }
          material.opacity = shouldDim ? 0.18 : 1;
          material.emissive?.set(isSelectedRoom ? '#39c9a6' : '#000000');
          if (material.emissive) material.emissiveIntensity = isSelectedRoom ? 0.45 : 0;
        });
      }
      if (child.isCSS2DObject) {
        const isSelected = child.userData.roomId === selectedRoomId;
        child.element.classList.toggle('is-selected', isSelected);
        child.element.classList.toggle('is-muted', dim && !isSelected);
      }
    });
  });
}
