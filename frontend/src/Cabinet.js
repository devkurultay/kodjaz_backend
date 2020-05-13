import React, { useState, useEffect } from 'react'
import SideNav, { Toggle, Nav, NavItem, NavIcon, NavText } from '@trendmicro/react-sidenav'
import { Router, Route, Link } from "react-router-dom"
import { createBrowserHistory } from 'history'
import classnames from 'classnames'

import axiosInstance from './axiosApi'

import Signup from './components/auth/signup'
import Login from './components/auth/login'
import Home from './components/home/Home'
import Form from './components/form/Form'

const history = createBrowserHistory()

const Cabinet = () => {
  const [ isExpanded, setIsExpanded ] = useState(false)
  return (
    <Router history={history}>
      <Route render={({ location, history }) => (
        <React.Fragment>
          <SideNav
            className="sidenav"
            onToggle={setIsExpanded}
            onSelect={(selected) => {
            const to = '/cabinet' + selected;
              if (location.pathname !== to) {
                history.push(to);
              }
            }}
          >
            <SideNav.Toggle />
            <SideNav.Nav defaultSelected="home">
              <NavItem eventKey="/">
                <NavIcon>
                  <i className="fa fa-fw fa-home" style={{ fontSize: '1.75em' }} />
                </NavIcon>
                <NavText>
                  Home
                </NavText>
              </NavItem>
              <NavItem eventKey="/form">
                <NavIcon>
                  <i className="fa fa-fw fa-form" style={{ fontSize: '1.75em' }} />
                </NavIcon>
                <NavText>
                  Form
                </NavText>
              </NavItem>
            </SideNav.Nav>
          </SideNav>
          <main className={classnames("main-content", { "margin-left-240": isExpanded })}>
            <Route path="/cabinet/login/" exact component={props => <Login />} />
            <Route path="/cabinet/signup/" exact component={props => <Signup />} />
            <Route path="/cabinet/" exact component={props => <Home />} />
            <Route path="/cabinet/form" component={props => <Form />} />
          </main>
        </React.Fragment>
      )}/>
    </Router>
  )
}

export default Cabinet;
