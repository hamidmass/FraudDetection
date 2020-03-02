const handleForm = e => {
    e.preventDefault();
    firebase
    .auth()
    .signInWithEmailAndPassword(email, password)
    .then(res => {
      if (res.user) Auth.setLoggedIn(true);
    })
    .catch(e => {
      setErrors(e.message);
    });
  };