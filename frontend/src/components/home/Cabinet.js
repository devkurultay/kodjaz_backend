import React, { useState, useEffect } from 'react'
import SideNav, { NavItem, NavIcon, NavText } from '@trendmicro/react-sidenav'
import { Route, useHistory, useLocation } from "react-router-dom"
import classnames from 'classnames'

import Home from './Home'
import ExerciseForm from '../form/ExerciseFormContainer'

const Cabinet = ({ logout, loadTracks, resetNewlyCreatedLessonId }) => {
  const history = useHistory()
  const location = useLocation()
  const [ isExpanded, setIsExpanded ] = useState(false)
  useEffect(() => {
    loadTracks()
    resetNewlyCreatedLessonId()
  }, [loadTracks, resetNewlyCreatedLessonId])

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
          <NavItem eventKey="logout" onClick={() => logout()}>
            <NavIcon>
              <i className="fa fa-fw fa-power-off" style={{ fontSize: '1.75em' }} />
            </NavIcon>
            <NavText>
              Logout
            </NavText>
          </NavItem>
        </SideNav.Nav>
      </SideNav>
      <main className={classnames("main-content mt-3 px-5", { "margin-left-240": isExpanded })}>
        <Route path="/" exact render={() => <Home />} />
        <Route path="/create-exercise/" render={() => <ExerciseForm />} />
        <Route path="/exercise/:exerciseId" render={() => <ExerciseForm />} />
      </main>
    </>
  )
}

export default Cabinet;
