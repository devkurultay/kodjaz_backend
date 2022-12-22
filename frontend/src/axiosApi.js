import axios from 'axios'
import Cookies from 'js-cookie'

const baseURL = 'http://localhost:8000/api/'
const cabinetURL = '/cabinet/'
const v1URL = '/v1/'

const axiosInstance = axios.create({
  baseURL: baseURL,
  timeout: 5000,
  headers: {
    'Authorization': Cookies.get('access_token') ? "Token " + Cookies.get('access_token') : null,
    'Content-Type': 'application/json',
    'accept': 'application/json'
  }
})

axiosInstance.interceptors.response.use(
  response => {
    return response
  },
  async error => {
    const errorResp = error.response
    if (isTokenExpired(errorResp ?? {})) {
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
  const errorMsgs = ['Given token not valid for any token type', 'Token has been expired.']
  return status === 401 && errorMsgs.includes(detail)
}

const getWrongCredentialsErrorMessages = (errorResp) => {
  const { data, status } = errorResp
  if (status > 401) {
    return []
  }
  const { email, password, detail } = data
  const errorMsg = []
  detail && errorMsg.push(detail)
  email && errorMsg.push(`Email: ${email?.[0]}`)
  password && errorMsg.push(`Password: ${password?.[0]}`)
  return errorMsg
}

const getTokensFromCookies = async () => {
  const accessToken= await Cookies.get('access_token')
  const refreshToken = await Cookies.get('refresh_token')
  return { accessToken, refreshToken }
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
    const { accessToken, refreshToken } = await getTokensFromCookies()
    if (!accessToken || !refreshToken) {
      return Promise.reject(error)
    }
    const { response: errorResponse } = error
    const resendOriginalRequest = new Promise(resolve => {
      addSubscriber(token => {
        errorResponse.config.headers.Authorization = 'Token ' + token
        resolve(axios(errorResponse.config))
      })
    })
    if(!isFetchingAccessTokenInProgress) {
      isFetchingAccessTokenInProgress = true
      const response = await axios.post(
        baseURL + 'token/refresh/',
        { refresh: refreshToken }
      )
      if (response && !response.data) {
        return Promise.reject(error)
      }
      const newAccessToken = response?.data?.access
      const newRefreshToken = response?.data?.refresh
      await setTokensToCookies(newAccessToken, newRefreshToken)
      axiosInstance.defaults.headers.Authorization = 'Token ' + newAccessToken
      isFetchingAccessTokenInProgress = false
      triggerSubscribers(newAccessToken)
    }
    return resendOriginalRequest
  } catch (e) {
    return Promise.reject(e)
  }
}

export default axiosInstance
