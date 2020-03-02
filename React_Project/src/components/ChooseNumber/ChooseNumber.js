import React, { Component } from 'react';
import styles from './ChooseNumber.css';
import {Form, FormGroup} from "reactstrap";

class ChooseNumber extends Component {
  // constructor(props){
  //   super(props);
  // }
  state = {
    phones: []
  };

  componentDidMount() {
    const options = {
      headers: {
        'Content-type': 'application/form-data',
        'Accept': 'application/json',
        'Access-Control-Allow-Origin' : "*",
        'Authorization': 'Bearer ' + sessionStorage.getItem("access_token")
      },
      method: 'GET',
    };
    fetch(`${process.env.REACT_APP_BASE_URL}user/phone?phone_type=${this.props.phone_type}`, options)
      .then(response => response.json())
      .then(response => {
        this.setState({phones: response.phones});
      }).catch(error => {
      console.log("Error while obtaining phone numbers: " + error.toString());
    })
  };

  save_number(number) {
    sessionStorage.setItem('phone_number', number);
  }

  render() {
    return (
      <Form className={styles.loginForm}>
        <FormGroup>
          <select>
            <option value="id">Choose Phone Number</option>
            {this.state.phones.map(phone => {
              return <option value={`number-${phone.phone_number}`} onClick={this.save_number(phone.phone_number)}>{phone.phone_number}</option>
            })}
          </select>
        </FormGroup>
      </Form>
    );
  }
}

export default ChooseNumber;

