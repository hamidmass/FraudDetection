import React, { Component } from 'react';
import { Route, Switch } from 'react-router-dom';
import Navbar from './components/Navbar/Navbar';

import Page1 from './containers/Page1/Page1';
import Call from './containers/Call_Page/Call/Call';
import Calling from './containers/Calling_Page/Calling';
import Auth from './containers/Auth/Auth';
import Register from './containers/Register/Register';
import AccountSettings from './containers/AccountSettings/AccountSettings';

class App extends Component {
  render() {
    return (
      <div id='root'>
        <Navbar />
        <Switch>
          <Route path="/Calling" component={Calling} />
          <Route path="/Call" component={Call} />
          <Route path="/AccountSettings" component={AccountSettings} />
          <Route path="/Register" component={Register} />
          <Route path="/Page1" component={Page1} />
          <Route path="/" exact component={Auth} />
        </Switch>
      </div>
    );
  }
}

export default App;

