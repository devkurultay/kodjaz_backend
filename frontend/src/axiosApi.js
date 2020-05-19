import axios from 'axios'
import Cookies from 'js-cookie'

const baseURL = '/api/'
const cabinetURL = '/cabinet/'
const v1URL = '/v1/'

const axiosInstance = axios.create({
  baseURL: baseURL,
  timeout: 5000,
  headers: {
    'Authorization': Cookies.get('access_token') ? "JWT " + Cookies.get('access_token') : null,
    'Content-Type': 'application/json',
    'accept': 'application/json'
  }
})

axiosInstance.interceptors.response.use(
  response => response,
  error => {
    const errorResp = error.response
    if (isTokenExpired(errorResp)) {
      return refreshTokenAndResendRequest(error)
    }
    const wrongCredentialsErrors = getWrongCredentialsErrorMessages(errorResp)
    if (wrongCredentialsErrors.length > 0) {
      return Promise.reject(wrongCredentialsErrors)
    }
    return Promise.reject(error)
  }
)

const isTokenExpired = (errorResp) => {
  const { data, status } = errorResp
  const { detail } = data
  return status === 401 && detail === "Token has been expired."
}

const getWrongCredentialsErrorMessages = (errorResp) => {
  const { data, status } = errorResp
  if (status > 401) {
    return []
  }
  const { username, password, detail } = data
  const errorMsg = []
  detail && errorMsg.push(detail)
  username && errorMsg.push(`Username: ${username?.[0]}`)
  password && errorMsg.push(`Password: ${password?.[0]}`)
  return errorMsg
}

const getTokensFromCookies = () => {
  const token = Cookies.get('access_token')
  const refreshToken = Cookies.get('refresh_token')
  return { token, refreshToken }
}

const setTokensToCookies = async (access_token, refresh_token) => {
  await Cookies.set('access_token', access_token)
  await Cookies.set('refresh_token', refresh_token)
}

let isFetchingAccessTokenInProgress = false

let subscribers = []

const addSubscriber = (cb) => {
  subscribers.push(cb)
}

const triggerSubscribers = (accessToken) => {
  subscribers.forEach(cb => cb(accessToken))
  subscribers = []
}

const refreshTokenAndResendRequest = async (error) => {
  try {
    const { accessToken, refreshToken } = getTokensFromCookies()
    if (!accessToken || !refreshToken) {
      return Promise.reject(error)
    }
    const { response: errorResponse } = error
    const resendOriginalRequest = new Promise(resolve => {
      addSubscriber(token => {
        errorResp.config.headers.Authorization = 'JWT ' + token
        resolve(axios(errorResp.config))
      })
    })
    if(!isFetchingAccessTokenInProgress) {
      isFetchingAccessTokenInProgress = true
      const response = await axios.post(
        '/token/refresh/',
        { refresh: refreshToken }
      )
      if (response && !response.data) {
        return Promise.reject(error)
      }
      const newAccessToken = response?.data?.access
      const newRefreshToken = response?.data?.refresh
      await setTokensToCookies(newAccessToken, newRefreshToken)
      isFetchingAccessTokenInProgress = false
      triggerSubscribers(newAccessToken)
    }
    return resendOriginalRequest
  } catch (e) {
    return Promise.reject(e)
  }
}

export default axiosInstance
