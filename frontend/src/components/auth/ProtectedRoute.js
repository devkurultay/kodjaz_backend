import React, { useEffect } from 'react'
import Cookies from 'js-cookie'
import { connect } from 'react-redux'
import { bindActionCreators } from 'redux'
import { Route } from "react-router-dom"
import axiosInstance from '../../axiosApi'
import { checkIsAuth } from '../../actions/login'
import AbsoluteRedirect from '../common/AbsoluteRedirect'

const ProtectedRoute = ({ component: Component, isAuthenticated, checkIsAuth, ...rest }) => {
  const { location } = rest

  useEffect(() => {
    // Call on mount
    checkIsAuth()
  }, [])

  useEffect(() => {
    // Call every time location changes
    checkIsAuth()
  }, [ location ])

  if (isAuthenticated === null) {
    // TODO(murat): Show beautiful loading spinner
    return <div>Loading</div>
  }
  const PATH_TO_REDIRECT_TO = '/accounts/login/?next=/cabinet/'
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
