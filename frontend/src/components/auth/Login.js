import React, { Component } from 'react'
import Cookies from 'js-cookie'
import { connect } from 'react-redux'
import { bindActionCreators } from 'redux'
import { Redirect } from 'react-router-dom'
import { login } from '../../actions/login'

import axiosInstance from '../../axiosApi'

class Login extends Component {
  constructor(props) {
    super(props)
    this.state = {email: "", password: ""}

    this.handleChange = this.handleChange.bind(this)
    this.handleSubmit = this.handleSubmit.bind(this)
    this.renderError = this.renderError.bind(this)
  }

  handleChange(event) {
    this.setState({[event.target.name]: event.target.value});
  }

  async handleSubmit(event) {
    event.preventDefault();
    try {
      this.props.login(this.state.email, this.state.password)
      return
    } catch (error) {
      throw error
    }
  }

  renderError () {
    return this.props.loginError.map(e => <div key={e}>{e}</div>)
  }

  render() {
    if (this.props.isAuthenticated) {
      // TODO: get `from` path and redirec there
      // return <Redirect to={{ pathname: '/' }} />
    }
    return (
      <div>
        Login
        { this.props.loginError.length > 0 ? this.renderError() : null }
        <form onSubmit={this.handleSubmit}>
          <label>
            Email:
            <input name="email" type="email" value={this.state.email} onChange={this.handleChange}/>
          </label>
          <label>
            Password:
            <input name="password" type="password" value={this.state.password} onChange={this.handleChange}/>
          </label>
          <input type="submit" value="Submit"/>
        </form>
      </div>
    )
  }
}

const mapStateToProps = state => {
  return {
    isAuthenticated: state.isAuthenticated,
    loginError: state.loginError
  }
}

const mapDispatchToProps = dispatch => {
  return bindActionCreators(
    { login },
    dispatch
  )
}

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(Login)
