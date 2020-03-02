import React, { Component }  from 'react';
import Grid from '@material-ui/core/Grid';
import TextField from '@material-ui/core/TextField';
import styles from './AccountSettings.css';
import { Button } from 'reactstrap';
import { auth } from '../../helpers/firebase';

const INITIAL_STATE = {
    firstName: "",
    lastName: "",
    number: "",
    addressOne: "",
    addressTwo: "",
    city: "",
    zip: "",
    country: "",
    file: ""
};

// nice way of changing properties
const byPropKey = (propertyName, value) => () => ({
    [propertyName]: value
});

const encodeGetParams = p => 
  Object.entries(p).map(kv => kv.map(encodeURIComponent).join("=")).join("&");

// TODO: phone number nationality
// TODO: civility?
class Info extends Component {
    state = {
        ...INITIAL_STATE
    };
    sendEmailVerification = () => {
		console.log("Sending verification");
		auth.currentUser.sendEmailVerification({
			url: "http://localhost:3000"
		});
	}
    onSubmit = event => {
        const { firstName, lastName, 
            number, addressOne, addressTwo, city, zip, country, file } = this.state;
        
        const firebaseId = sessionStorage.getItem('firebase_id');
        const email = sessionStorage.getItem('email');
        
        // Create a user in the database
        const values = {
            'email': email,
            'phone_number': number,
            'phone_number_nationality': 'FI',
            'first_name': firstName,
            'last_name': lastName,
            'civility': '',
            'street': addressOne + "\n"+ addressTwo,
            'zip': zip,
            'city': city,
            'country': country,
            'firebase_id': firebaseId
        }

        const options = {
            headers: {
              'Content-type': 'application/json',
              'Accept': 'application/json',
              'Access-Control-Allow-Origin' : "*"
            },
            method: 'GET'
        }
        
        // Add User
        fetch(`${process.env.REACT_APP_BASE_URL}add_user?` + encodeGetParams(values), options)
            .then(response => {
                return response.text()
            })
            .then(response => {
                console.log("Got response" + response);
                const data = JSON.parse(response);
                console.log(data);

                if (data[1] !== 200) {
                    console.log("Message: " + data[0].message)
                    console.log("Error");
                    return;
                }

                // Store the JWT tokens
                sessionStorage.setItem("access_token", data[0].access_token);
                sessionStorage.setItem("refresh_token", data[0].refresh_token);

                this.setState({
                    ...INITIAL_STATE
                });

                // Upload the identification
                const fileUploadOption = {
                    headers: {
                      'Content-type': 'multipart/form-data',
                      'Access-Control-Allow-Origin': '*',
                      'Referrer-Policy': 'origin-when-cross-origin',
                      'Authorization': 'Bearer ' + sessionStorage.getItem("access_token")
                    },
                    method: 'POST',
                    body: {
                        "file" : file
                    }
                }

                const identification_params = {
                    "email": email
                }

                fetch(`${process.env.REACT_APP_BASE_URL}upload_user_identification?`+ encodeGetParams(identification_params), fileUploadOption)
                    .then(response => {
                        return response.text()
                    })
                    .then(response => {
                        console.log("File uploaded: " + response);
                        
                        // Send a message to the user
                        this.sendEmailVerification();
                        
                        // We return to the login page
                        this.props.history.push("");
                    })
                    .catch(error => {
                        console.log("File Upload Error: " + error);
                    })

            })
            .catch(error => {
                console.log("DB error: " + error);
            })

        event.preventDefault();
    };
    render () {
        const { firstName, lastName, 
            number, addressOne, addressTwo, city, zip, country } = this.state;

        return (
            <React.Fragment>
                <form className={styles.Register} onSubmit={this.onSubmit}>
                    <div className={styles.logoName}>Personal Info</div>
                    <Grid container spacing={3} className={styles.textField}>
                        <Grid item xs={12} sm={6}>
                        <TextField
                            required
                            id="outlined-basic"
                            name="firstName"
                            label="First name"
                            fullWidth
                            autoComplete="fname"
                            value={firstName}
                            onChange={e =>
                                this.setState(byPropKey("firstName", e.target.value))
                            }
                        />
                        </Grid>
                        <Grid item xs={12} sm={6}>
                        <TextField
                            required
                            id="lastName"
                            name="lastName"
                            label="Last name"
                            fullWidth
                            autoComplete="lname"
                            value={lastName}
                            onChange={e =>
                                this.setState(byPropKey("lastName", e.target.value))
                            }
                        />
                        </Grid>
                        <Grid item xs={12}>
                        <TextField
                            required
                            id="standard-number"
                            label="Number"
                            type="tel"
                            fullWidth
                            autoComplete="current-number"
                            value={number}
                            onChange={e =>
                                this.setState(byPropKey("number", e.target.value))
                            }
                        />
                        </Grid>
                        <Grid item xs={12}>
                        <TextField
                            required
                            id="address1"
                            name="address1"
                            label="Address line 1"
                            fullWidth
                            autoComplete="billing address-line1"
                            value={addressOne}
                            onChange={e =>
                                this.setState(byPropKey("addressOne", e.target.value))
                            }
                        />
                        </Grid>
                        <Grid item xs={12}>
                        <TextField
                            id="address2"
                            name="address2"
                            label="Address line 2"
                            fullWidth
                            autoComplete="billing address-line2"
                            value={addressTwo}
                            onChange={e =>
                                this.setState(byPropKey("addressTwo", e.target.value))
                            }
                        />
                        </Grid>
                        <Grid item xs={12} sm={6}>
                        <TextField
                            required
                            id="city"
                            name="city"
                            label="City"
                            fullWidth
                            autoComplete="billing address-level2"
                            value={city}
                            onChange={e =>
                                this.setState(byPropKey("city", e.target.value))
                            }
                        />
                        </Grid>
                        <Grid item xs={12} sm={6}>
                        <TextField id="state" name="state" label="State/Province/Region" fullWidth />
                        </Grid>
                        <Grid item xs={12} sm={6}>
                        <TextField
                            required
                            id="zip"
                            name="zip"
                            label="Zip / Postal code"
                            fullWidth
                            autoComplete="billing postal-code"
                            value={zip}
                            onChange={e =>
                                this.setState(byPropKey("zip", e.target.value))
                            }
                        />
                        </Grid>
                        <Grid item xs={12} sm={6}>
                        <TextField
                            required
                            id="country"
                            name="country"
                            label="Country"
                            fullWidth
                            autoComplete="billing country"
                            value={country}
                            onChange={e =>
                            this.setState(byPropKey("country", e.target.value))
                            }
                        />
                        </Grid>
                        <Grid item xs={12} sm={6}>
                        <TextField 
                            required
                            defaultValue="Upload Passport/ID"
                            id="passportId"
                            fullWidth
                        />
                        </Grid>
                        <Grid item xs={12} sm={6}>
                        <TextField 
                            required
                            type="file" 
                            name="file" 
                            id="exampleFile"
                            color="black"
                            fullWidth
                        />
                        </Grid>
                        <Grid item xs={12}>
                        <Button className={styles.Button}>Send</Button>
                        </Grid>
                    </Grid>
                </form>
            </React.Fragment>
        );
    }
}

export default Info;