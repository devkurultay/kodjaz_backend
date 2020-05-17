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

const isProtectedUrl = (url) => {
  const isTokenRefresh = url === baseURL + 'token/refresh/'
  const isCabinet = url === cabinetURL
  const isStartsWithProtected = url.startsWith(v1URL)
  return isTokenRefresh || isCabinet || isStartsWithProtected
}

axiosInstance.interceptors.response.use(
  response => response,
  error => {
    const errorResp = error.response
    if (isTokenExpired(errorResp)) {
      return refreshTokenAndResendRequest(error)
    }
    if (isWrongCredentials(errorResp)) {
      return Promise.reject(errorResp?.data?.detail)
    }
    return Promise.reject(error)
  }
)

const isTokenExpired = (errorResp) => {
  const { data, status } = errorResp
  const { detail } = data
  return status === 401 && detail === "Token has been expired."
}

const isWrongCredentials = (errorResp) => {
  const { data, status, statusText } = errorResp
  return data?.detail === 'No active account found with the given credentials' &&
    status === 401 &&
    statusText === 'Unauthorized'
}

const getRefreshTokenFromCookies = async () => {
  const token = await Cookies.get('access_token')
  const refreshToken = await Cookies.get('refresh_token')
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
    const { response: errorResponse } = error
	  const { accessToken, refreshToken } = await getRefreshTokenFromCookies()
    if (!accessToken || !refreshToken) {
      return Promise.reject(error)
    }
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
