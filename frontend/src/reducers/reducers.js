const initialState = {
  isAuthenticated: null,
  loginError: [],
  currentExercise: {},
}

function cabinet(state = initialState, action) {
  switch(action.type) {
    case 'LOG_IN':
      return {
        ...state,
        loginError: [],
        isAuthenticated: true
      }
    case 'FAILED_TO_LOG_IN':
      return {
        ...state,
        isAuthenticated: false,
        loginError: action.payload
      }
    case 'LOAD_EXERCISE':
      return {
        ...state,
        currentExercise: action.payload
      }
    default:
      return state
  }
}

export default cabinet
