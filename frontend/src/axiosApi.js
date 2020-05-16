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
        const originalRequest = error.config

        // Prevent infinite loops early
        if (error.response.status === 401 && isProtectedUrl(originalRequest.url)) {
            window.location.href = '/cabinet/login/'
            return Promise.reject(error)
        }

        if (error.response.data.code === "token_not_valid" &&
            error.response.status === 401 && 
            error.response.statusText === "Unauthorized")
            {
                const refreshToken = Cookies.get('refresh_token');

                if (refreshToken){
                    const tokenParts = JSON.parse(atob(refreshToken.split('.')[1]));

                    // exp date in token is expressed in seconds, while now() returns milliseconds:
                    const now = Math.ceil(Date.now() / 1000);
                    console.log(tokenParts.exp);

                    if (tokenParts.exp > now) {
                        return axiosInstance
                        .post('/token/refresh/', {refresh: refreshToken})
                        .then((response) => {
            
                            Cookies.set('access_token', response.data.access);
                            Cookies.set('refresh_token', response.data.refresh);
            
                            axiosInstance.defaults.headers['Authorization'] = "JWT " + response.data.access;
                            originalRequest.headers['Authorization'] = "JWT " + response.data.access;
            
                            return axiosInstance(originalRequest);
                        })
                        .catch(err => {
                            console.log(err)
                        });
                    }else{
                        console.log("Refresh token is expired", tokenParts.exp, now);
                        window.location.href = '/cabinet/login/';
                    }
                }else{
                    console.log("Refresh token not available.")
                    window.location.href = '/cabinet/login/';
                }
        }
      
     
      // specific error handling done elsewhere
      return Promise.reject(error);
  }
);

export default axiosInstance
