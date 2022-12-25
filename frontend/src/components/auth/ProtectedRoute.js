import React, { useEffect } from 'react'
import { connect } from 'react-redux'
import { bindActionCreators } from 'redux'
import { Route } from "react-router-dom"
import { checkIsAuth } from '../../actions/login'
import AbsoluteRedirect from '../common/AbsoluteRedirect'

const ProtectedRoute = ({ component: Component, isAuthenticated, checkIsAuth, ...rest }) => {
  const { location } = rest

  useEffect(() => {
    // Call on mount
    checkIsAuth()
  }, [checkIsAuth])

  useEffect(() => {
    // Call every time location changes
    checkIsAuth()
  }, [ location, checkIsAuth ])

  if (isAuthenticated === null) {
    // TODO(murat): Show beautiful loading spinner
    return <div>Loading</div>
  }
  const PATH_TO_REDIRECT_TO = '/login/?next=/'
  return (
    <Route {...rest} render={(props) => (
      isAuthenticated
        ? <Component {...props} />
        : <AbsoluteRedirect to={PATH_TO_REDIRECT_TO} />   
    )} />
  )
}

const mapStateToProps = (state) => {
  return {
    isAuthenticated: state.isAuthenticated
  }
}

const mapDispatchToProps = (dispatch) => {
  return bindActionCreators(
    { checkIsAuth },
    dispatch
  )
}

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(ProtectedRoute)
