const initialState = {
  isAuthenticated: null,
  loginError: [],
  currentExercise: {},
  entityLoadingError: '',
  isLoadTracksPending: false,
  isLoadLessonsPending: false,
  isLoadExercisesPending: false,
  isSaveTrackPending: false,
  isSaveExercisePending: false,
  saveExerciseError: [],
  tracks: [],
  lessons: [],
  exercises: [],
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
    case 'LOAD_TRACKS_PENDING':
      return {
        ...state,
        isLoadTracksPending: true
      }
    case 'LOAD_TRACKS_FULFILLED':
      return {
        ...state,
        isLoadTracksPending: false,
        tracks: action.payload.data
      }
    case 'LOAD_LESSONS_PENDING':
      return {
        ...state,
        isLoadLessonsPending: true
      }
    case 'LOAD_LESSONS_FULFILLED':
      return {
        ...state,
        isLoadLessonsPending: false,
        lessons: action.payload.data
      }
    case 'LOAD_EXERCISES_PENDING':
      return {
        ...state,
        isLoadExercisesPending: true
      }
    case 'LOAD_EXERCISES_FULFILLED':
      return {
        ...state,
        isLoadExercisesPending: false,
        exercises: action.payload.data
      }
    case 'SAVE_TRACK_PENDING':
      return {
        ...state,
        isSaveTrackPending: true
      }
    case 'SAVE_TRACK_FULFILLED':
      const updatedTrack = action.payload.data
      const tracks = state.tracks.reduce((acc, tr, ind) => {
        if (tr.id === updatedTrack.id) {
          acc.push(updatedTrack)
        } else {
          acc.push(tr)
        }
        return acc
      }, [])
      return {
        ...state,
        isSaveTrackPending: false,
        tracks
      }
    case 'SAVE_EXERCISE_PENDING':
      return {
        ...state,
        isSaveExercisePending: true,
        saveExerciseError: [],
      }
    case 'SAVE_EXERCISE_FULFILLED':
      const updatedExercise = action.payload.data
      const exercises = state.exercises.reduce((acc, ex, ind) => {
        if (ex.id === updatedExercise.id) {
          acc.push(updatedExercise)
        } else {
          acc.push(ex)
        }
        return acc
      }, [])
      return {
        ...state,
        isSaveExercisePending: false,
        exercises
      }
    case 'SAVE_EXERCISE_ERROR':
      return {
        ...state,
        isSaveExercisePending: false,
        saveExerciseError: action.payload
      }
    default:
      return state
  }
}

export default cabinet
