// auth.js — simple Firebase Web Auth helpers (ES module)
// Usage:
//   <script type="module" src="/assets/js/auth.js"></script>
//   import { initFirebase, signInWithGoogle, signOutUser, getIdToken } from './assets/js/auth.js'

/*
  Note: This file dynamically imports Firebase v9 modular SDK from official CDN.
  Ensure pages load it as a module (type="module") or use a bundler.
*/

export async function initFirebase(firebaseConfig) {
  // firebaseConfig example:
  // { apiKey:"...", authDomain:"...", projectId:"...", appId:"..." }
  if (!firebaseConfig) throw new Error("firebaseConfig required");
  const { initializeApp } = await import('https://www.gstatic.com/firebasejs/9.22.1/firebase-app.js');
  const { getAuth, GoogleAuthProvider } = await import('https://www.gstatic.com/firebasejs/9.22.1/firebase-auth.js');

  if (!window.__aips_firebase_app) {
    window.__aips_firebase_app = initializeApp(firebaseConfig);
    window.__aips_firebase_auth = getAuth(window.__aips_firebase_app);
    window.__aips_firebase_provider = new GoogleAuthProvider();
  }
  return true;
}

export async function signInWithGoogle() {
  const { signInWithPopup } = await import('https://www.gstatic.com/firebasejs/9.22.1/firebase-auth.js');
  if (!window.__aips_firebase_auth || !window.__aips_firebase_provider) {
    throw new Error("Firebase not initialized. Call initFirebase(firebaseConfig) first.");
  }
  const result = await signInWithPopup(window.__aips_firebase_auth, window.__aips_firebase_provider);
  // result.user contains user info
  return result.user;
}

export async function signOutUser() {
  const { signOut } = await import('https://www.gstatic.com/firebasejs/9.22.1/firebase-auth.js');
  if (!window.__aips_firebase_auth) throw new Error("Firebase not initialized");
  await signOut(window.__aips_firebase_auth);
  return true;
}

export async function getIdToken(forceRefresh = false) {
  if (!window.__aips_firebase_auth || !window.__aips_firebase_auth.currentUser) {
    return null;
  }
  return await window.__aips_firebase_auth.currentUser.getIdToken(forceRefresh);
}

export function onAuthStateChanged(callback) {
  // callback receives (user) or null
  import('https://www.gstatic.com/firebasejs/9.22.1/firebase-auth.js').then(m => {
    if (!window.__aips_firebase_auth) {
      console.warn("Firebase not initialized before registering onAuthStateChanged");
      return;
    }
    m.onAuthStateChanged(window.__aips_firebase_auth, callback);
  });
}
