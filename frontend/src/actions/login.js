import Cookies from 'js-cookie'
import axiosInstance from "../axiosApi"

async function performLogin(username, password) {
  const response = await axiosInstance.post('/token/obtain/', {
    username: username,
    password: password
  })
  return response
}

function loginUser() {
  return {
    type: 'LOG_IN'
  }
}

function failToLogIn(error) {
  return {
    type: 'FAILED_TO_LOG_IN',
    payload: error
  }
}

export function login(username, password) {
  return function (dispatch) {
    return performLogin(username, password).then(
      (response) => dispatch(loginUser()),
      (error) => dispatch(failToLogIn(error))
    )
  }
}
