'use client';

import { useRouter } from 'next/navigation';

export default function JoinGame() {
  const router = useRouter();

  return (
    <div>
      <button onClick={() => router.push('/profile')}>
        Profile
      </button>
    </div>
  );
}