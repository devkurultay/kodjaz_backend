import React, { useState, useEffect } from 'react'
import SideNav, { Toggle, Nav, NavItem, NavIcon, NavText } from '@trendmicro/react-sidenav'
import { Route, useHistory, useLocation } from "react-router-dom"
import classnames from 'classnames'

import axiosInstance from './axiosApi'

import Home from './components/home/Home'
import ExerciseForm from './components/form/ExerciseForm'

const Cabinet = () => {
  const history = useHistory()
  const location = useLocation()
  const [ isExpanded, setIsExpanded ] = useState(false)
  return (
    <>
      <SideNav
        className="sidenav"
        onToggle={setIsExpanded}
        onSelect={(selected) => {
          if (location.pathname !== selected) {
            history.push(selected)
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
        </SideNav.Nav>
      </SideNav>
      <main className={classnames("main-content mt-3 px-5", { "margin-left-240": isExpanded })}>
        <Route path="/" exact render={() => <Home />} />
        <Route path="/exercise/:id" render={() => <ExerciseForm />} />
      </main>
    </>
  )
}

export default Cabinet;
