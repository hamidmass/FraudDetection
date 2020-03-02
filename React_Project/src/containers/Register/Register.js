import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import { auth, googleProvider, faceProvider } from "../../helpers/firebase";
import styles from './Register.css';
import { Button, Form, FormGroup, Input} from 'reactstrap';
import Google from '../../assets/images/Google.png';
import Facebook from '../../assets/images/Facebook.png';

const INITIAL_STATE = {
	email: "",
	password: "",
};

const byPropKey = (propertyName, value) => () => ({
    [propertyName]: value
});

class Register extends Component { 
	state = { ...INITIAL_STATE };

    onSubmit = event => {
		const { email, password } = this.state;
		console.log("Using email: " + email);

		auth
		  .createUserWithEmailAndPassword(email, password)
		  .then(data => {
			console.log("Successfull User creation");
			console.log("Firebase User ID :", data.user.uid);
			sessionStorage.setItem('firebase_id', data.user.uid);
			sessionStorage.setItem('email', data.user.email);
			// We go to the info page
			this.props.history.push("AccountSettings");
		  })
		  .catch(error => {
			  console.log("Standard Login error " + error);
		  });
	
		event.preventDefault();
	};

	googleLogin = event => {
		console.log("googe")
		auth
		  .signInWithPopup(googleProvider)
		  .then(data => {
			console.log("Google Login Successfull");
			console.log("Firebase User ID :", data.user.uid);
			sessionStorage.setItem('firebase_id', data.user.uid);
			sessionStorage.setItem('email', data.user.email);
			// We go to the info page
			this.props.history.push("AccountSettings");
		  })
		  .catch(error => {
			  console.log("Google Login error: " + error);
		  });

		event.preventDefault();
	};

	faceLogin = () => {
		auth
		  .signInWithPopup(faceProvider)
		  .then(data => {
			console.log("Facebook Login auth: " + data);
			console.log("Facebook User ID :", data.user.uid);
			sessionStorage.setItem('firebase_id', data.user.uid);
			this.getRefreshToken();
			// We go to the home page
			this.props.history.push("AccountSettings");
		  })
		  .catch(error => {
			  console.log("Facebook Login error: " + error);
		  });
	};

	render () {
		const { email, password} = this.state;

		return (
			<Form className={styles.loginForm}>
				<h1><span className={styles.logoName}>Register</span></h1>
				<FormGroup>
					<Input type="email" 
					placeholder="Choose an Email"
					value={email}
					onChange={e =>
					  this.setState(byPropKey("email", e.target.value))
					}></Input>
				</FormGroup>
				<FormGroup>
					<Input type="password" 
					placeholder="Choose a Password"
					value={password}
					onChange={e =>
					  this.setState(byPropKey("password", e.target.value))
					}></Input>
				</FormGroup>
				<Button className={styles.Button} onClick={this.onSubmit}>Register</Button>
				<div className={styles.line}><span>Or Sign In with</span></div>
				<div className={styles.FacebookGoogle}>
					<Button onClick={this.googleLogin}><img src={Google} className={styles.Google}/>Sign In with Google</Button>
					<Button onClick={this.faceLogin}><img src={Facebook} className={styles.Facebook}/>Sign In with Facebook</Button>
				</div>
			</Form>
		);
	}
}

export default Register;