import React, { Component } from 'react';
import { Button, Form, FormGroup, Input} from 'reactstrap';
import { Link } from 'react-router-dom';
import styles from './Auth.css';

class Auth extends Component {
    render () {
		return (
			<Form className={styles.loginForm}>
				<h1><span className={styles.logoName}>Se Connecter</span></h1>
				<FormGroup>
                    <Input required 
                    type="email" 
					placeholder="Email"
                    ></Input>
				</FormGroup>
				<FormGroup>
                    <Input required 
                    type="password" 
					placeholder="Password"
					></Input>
				</FormGroup>
				<Button className={styles.Button} onClick={this.onSubmit}>Se Connecter</Button>
				<div className="text-center">
					<Link to="/Register">
						<a>Creat New Account</a>
					</Link>
				</div>
			</Form>
		);
	}
}

export default Auth;