const initialState = {
  isAuthenticated: null,
  loginError: [],
  currentExercise: {},
  entityLoadingError: '',
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
        entityLoadingError: '',
        currentExercise: action.payload
      }
    case 'FAILED_TO_LOAD':
      return {
        ...state,
        entityLoadingError: action.payload
      }
    default:
      return state
  }
}

export default cabinet
