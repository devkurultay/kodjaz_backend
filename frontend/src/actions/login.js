import Cookies from 'js-cookie'
import axiosInstance from "../axiosApi"

async function getTokens () {
  const refreshToken = await Cookies.get('refresh_token')
  const accessToken = await Cookies.get('access_token')
  return { refreshToken, accessToken }
}

function setTokens (accessToken, refreshToken) {
  Cookies.set('access_token', accessToken)
  Cookies.set('refresh_token', refreshToken)
}

async function performLogin(email, password) {
  const response = await axiosInstance.post('token/obtain/', {
    email: email,
    password: password
  })
  const newAccessToken = response?.data?.access
  const newRefreshToken = response?.data?.refresh
  setTokens(newAccessToken, newRefreshToken)
  axiosInstance.defaults.headers.Authorization = 'JWT ' + newAccessToken
  return response
}

async function performIsAuthCheck () {
  const { refreshToken, accessToken } = await getTokens()
  if (accessToken) {
    const tokenParts = JSON.parse(atob(refreshToken.split('.')[1]))
    // exp date in token is expressed in seconds, while now() returns milliseconds:
    const now = Math.ceil(Date.now() / 1000)
    if (tokenParts.exp > now) {
      return Promise.resolve(true)
    } else {
      return Promise.reject('Token expired')
    }
  }
  return Promise.reject('No token found')
}

function loginUser() {
  return {
    type: 'LOG_IN'
  }
}

function failToLogIn(error = []) {
  return {
    type: 'FAILED_TO_LOG_IN',
    payload: error
  }
}

export function login(email, password) {
  return function (dispatch) {
    return performLogin(email, password).then(
      (response) => dispatch(loginUser()),
      (error) => dispatch(failToLogIn(error))
    )
  }
}

export function checkIsAuth() {
  return function(dispatch) {
    return performIsAuthCheck().then(
      (response) => dispatch(loginUser()),
      (error) => dispatch(failToLogIn())
    )
  }
}

export function logout() {
  const refreshToken = Cookies.get('refresh_token')
  return function(dispatch) {
    return dispatch({
      type: 'LOGOUT',
      payload: axiosInstance.post(`/logout/`, { 'refresh': refreshToken })
    })
  }
}
