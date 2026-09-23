import { Suspense, useRef, useState, memo } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { MeshDistortMaterial, Sphere, Points, PointMaterial, Preload } from '@react-three/drei';
import * as THREE from 'three';

// Core distorted sphere. Rotation and distortion are driven inside
// useFrame (imperative, off the React render cycle) rather than useState,
// per the "never useState for continuous values" rule — this keeps 60fps
// even while the pointer is moving.
function Core() {
  const meshRef = useRef();
  const pointer = useRef({ x: 0, y: 0 });

  useFrame((state, delta) => {
    if (!meshRef.current) return;
    // Gentle idle rotation, always running.
    meshRef.current.rotation.y += delta * 0.12;
    meshRef.current.rotation.x += delta * 0.03;

    // Pointer influence, spring-lerped toward the target so movement feels
    // physical rather than snapping directly to the cursor.
    const targetX = (state.pointer.y * Math.PI) / 10;
    const targetY = (state.pointer.x * Math.PI) / 8;
    pointer.current.x = THREE.MathUtils.lerp(pointer.current.x, targetX, 0.04);
    pointer.current.y = THREE.MathUtils.lerp(pointer.current.y, targetY, 0.04);
    meshRef.current.rotation.x += pointer.current.x * delta;
    meshRef.current.rotation.y += pointer.current.y * delta;
  });

  return (
    <Sphere ref={meshRef} args={[1.4, 128, 128]}>
      <MeshDistortMaterial
        color="#173047"
        emissive="#0d1a26"
        distort={0.42}
        speed={1.6}
        roughness={0.15}
        metalness={0.4}
        clearcoat={0.6}
      />
    </Sphere>
  );
}

// A thin halo ring to suggest "scope" — eight departments orbiting one core.
function Halo() {
  const ref = useRef();
  useFrame((_, delta) => {
    if (ref.current) ref.current.rotation.z += delta * 0.05;
  });
  return (
    <mesh ref={ref} rotation={[Math.PI / 2.4, 0, 0]}>
      <torusGeometry args={[2.15, 0.008, 16, 100]} />
      <meshBasicMaterial color="#21D4B4" transparent opacity={0.35} />
    </mesh>
  );
}

function Particles() {
  const ref = useRef();
  const [positions] = useState(() => {
    const arr = new Float32Array(240 * 3);
    for (let i = 0; i < 240; i++) {
      const r = 2.6 + Math.random() * 1.4;
      const theta = Math.random() * Math.PI * 2;
      const phi = Math.acos(2 * Math.random() - 1);
      arr[i * 3] = r * Math.sin(phi) * Math.cos(theta);
      arr[i * 3 + 1] = r * Math.sin(phi) * Math.sin(theta);
      arr[i * 3 + 2] = r * Math.cos(phi);
    }
    return arr;
  });

  useFrame((_, delta) => {
    if (ref.current) ref.current.rotation.y += delta * 0.02;
  });

  return (
    <Points ref={ref} positions={positions} stride={3} frustumCulled>
      <PointMaterial transparent color="#5C8DFF" size={0.015} sizeAttenuation depthWrite={false} opacity={0.55} />
    </Points>
  );
}

/**
 * OrbScene renders the "One" mark: a single distorted sphere at the
 * center, a thin halo, and a light particle field — one core, eight
 * departments orbiting it, quietly. Isolated as its own leaf component
 * (per taste-skill interactivity isolation) so nothing else in the tree
 * re-renders on pointer movement.
 */
function OrbScene({ className = '' }) {
  return (
    <div className={className} aria-hidden="true">
      <Canvas
        camera={{ position: [0, 0, 5], fov: 42 }}
        dpr={[1, 1.75]}
        gl={{ antialias: true, alpha: true }}
      >
        <ambientLight intensity={0.4} />
        <pointLight position={[4, 3, 5]} intensity={40} color="#5C8DFF" />
        <pointLight position={[-4, -2, -3]} intensity={20} color="#21D4B4" />
        <Suspense fallback={null}>
          <Core />
          <Halo />
          <Particles />
          <Preload all />
        </Suspense>
      </Canvas>
    </div>
  );
}

export default memo(OrbScene);
