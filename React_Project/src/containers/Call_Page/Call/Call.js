import React, { Component } from 'react';

import Keyboard from '../Keyboard/Keyboard';
import styles from './Call.css';
import axios from 'axios'
import ChooseNumber from '../../../components/ChooseNumber/ChooseNumber'

class Call extends Component {
    state = {
        numberClicked: [],
        phones: []
    }

    clickNumber = (number) => {
        let callNumber = this.state.numberClicked
        callNumber.push(number)
        console.log(callNumber)
        this.setState({
            numberClicked: callNumber
        })
    }

    deleteNumber = () => {
        let callNumber = this.state.numberClicked
        callNumber.pop()
        console.log(callNumber)
        this.setState({
            numberClicked: callNumber
        })
    }

    call = () => {
        let callNumber = this.state.numberClicked;
        let form = new FormData();
        console.log("phoneeeee: " + sessionStorage.getItem("phone_number"))
        form.append('From', sessionStorage.getItem("phone_number"));
        form.append('To', callNumber.join(''));
        const options = {
            headers: {
                'Content-type': 'application/form-data',
                'Accept': 'application/json',
                'Access-Control-Allow-Origin' : "*",
                'Authorization': 'Bearer ' + sessionStorage.getItem("access_token")
            },
            method: 'POST',
        };
        console.log("url: " + process.env.BASE_URL);
        console.log("token: " + sessionStorage.getItem("access_token"));
        axios.post(`${process.env.REACT_APP_BASE_URL}outbound-call`, form, options)
          .then(response => {
              console.log("call started");
          }).catch(error => {
              console.log("File Upload Error: " + error.toString());
          })
    };

    render(){
        return (
            <div className={styles.Center}>
                <ChooseNumber phone_type={'voice'}/>
                <div className={styles.Rectangle}>{this.state.numberClicked}</div>
                <Keyboard
                    numbers={this.state.numbers}
                    action={this.clickNumber}
                    remove={this.deleteNumber}
                    call={this.call}
                />
            </div>
        )};
}

export default Call;
