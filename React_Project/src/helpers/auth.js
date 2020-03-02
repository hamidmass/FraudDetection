import { auth, googleProvider } from "./firebase"; 

export const doCreateUserWithEmailAndPassword = (email, password) =>
  auth.createUserWithEmailAndPassword(email, password);

export const doSignInWithEmailAndPassword = (email, password) =>
  auth.signInWithEmailAndPassword(email, password);

export const doSignOut = () => auth.signOut();

export const doPasswordReset = email => auth.sendPasswordResetEmail(email);

export const doPasswordChange = password =>
  auth.currentUser.updatePassword(password);

export const doGoogleSignIn = () => auth.signInWithPopup(googleProvider);