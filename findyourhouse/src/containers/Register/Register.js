import React, { Component } from 'react';
import styles from './Register.css';
import { Button, Form, FormGroup, Input} from 'reactstrap';



class Register extends Component { 
	render () {
		return (
			<Form className={styles.loginForm}>
				<h1><span className={styles.logoName}>Créer un Compte</span></h1>
				<FormGroup>
                    <Input required
                    type="email" 
					placeholder="Choose an Email"
                    ></Input>
				</FormGroup>
				<FormGroup>
                    <Input required
                    type="password" 
					placeholder="Choose a Password"
                    ></Input>
				</FormGroup>
				<Button className={styles.Button}>Créer un Compte</Button>
			</Form>
		);
	}
}

export default Register;

