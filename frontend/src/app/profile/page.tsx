'use client';
import { RequireAuth } from "../../../components/require_auth";

export default function Profile() {

  return (
    <RequireAuth>
      <div>
        <h1>Profile</h1>
      </div>
    </RequireAuth>
  );
}