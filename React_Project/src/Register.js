const handleForm = e => {
    e.preventDefault();
    firebase
      .auth()
      .createUserWithEmailAndPassword(email, password)
      .then(res => {
        if (res.user) Auth.setLoggedIn(true);
      })
      .catch(e => {
        setErrors(e.message);
      });
  };