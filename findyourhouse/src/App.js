import React, { Component } from 'react';
import { Route, Switch } from 'react-router-dom';

import MainPage from './containers/MainPage/MainPage';
import Auth from './containers/Auth/Auth';
import Register from './containers/Register/Register';

class App extends Component {
  render() {
    return (
      <div id='root'>
        <Switch>
          <Route path="/Register" component={Register} />
          <Route path="/MainPage" component={MainPage} />
          <Route path="/" exact component={Auth} />
        </Switch>
      </div>
    );
  }
}

export default App;

