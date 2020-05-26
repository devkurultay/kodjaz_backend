import axiosInstance from "../axiosApi"

async function performExerciseLoading(id) {
  const response = await axiosInstance.get(`/v1/exercises/${id}/`)
  return response?.data
}

function getExercise(data) {
  return {
    type: 'LOAD_EXERCISE',
    payload: data
  }
}

function failedToLoad(error) {
  return {
    type: 'FAILED_TO_LOAD',
    payload: error
  }
}

function failedToSaveExercise(error) {
  const errors = error?.response?.data
  return {
    type: 'SAVE_EXERCISE_ERROR',
    payload: errors
  }
}

export function loadExercise(id) {
  return function (dispatch) {
    return performExerciseLoading(id).then(
      (data) => dispatch(getExercise(data)),
      (error) => dispatch(failedToLoad(error))
    )
  }
}

export function saveExercise(id, exercise) {
  return function (dispatch) {
    return dispatch({
      type: 'SAVE_EXERCISE',
      payload: axiosInstance.put(`/v1/exercises/${id}/`, exercise)
    }).catch(
      (error) => dispatch(failedToSaveExercise(error))
    )
  }
}

export function saveTrack(id, track) {
  return function(dispatch) {
    return dispatch({
      type: 'SAVE_TRACK',
      payload: axiosInstance.put(`/v1/tracks/${id}/`, track)
    })
  }
}

<<<<<<< HEAD
export function createTrack(track) {
  return function(dispatch) {
    return dispatch({
      type: 'CREATE_TRACK',
      payload: axiosInstance.post(`/v1/tracks/`, track)
    })
  }
}

export function createUnit(unit) {
  return function(dispatch) {
    return dispatch({
      type: 'CREATE_UNIT',
      payload: axiosInstance.post(`/v1/units/`, unit)
    })
  }
}

export function createLesson(lesson) {
  return function(dispatch) {
    return dispatch({
      type: 'CREATE_LESSON',
      payload: axiosInstance.post(`/v1/lessons/`, lesson)
    })
  }
}

export function createExercise(exercise) {
  return function(dispatch) {
    return dispatch({
      type: 'CREATE_EXERCISE',
      payload: axiosInstance.post(`/v1/exercises/`, exercise)
    }).catch(
      (error) => dispatch(failedToSaveExercise(error))
    )
  }
}

=======
>>>>>>> Make it possible to edit Unit
export function saveUnit(id, unit) {
  return function(dispatch) {
    return dispatch({
      type: 'SAVE_UNIT',
      payload: axiosInstance.put(`/v1/units/${id}/`, unit)
    })
  }
}

<<<<<<< HEAD
export function saveLesson(id, lesson) {
  return function(dispatch) {
    return dispatch({
      type: 'SAVE_LESSON',
      payload: axiosInstance.put(`/v1/lessons/${id}/`, lesson)
    })
  }
}

=======
>>>>>>> Make it possible to edit Unit
export function loadTracks() {
  return function(dispatch) {
    return dispatch({
      type: 'LOAD_TRACKS',
      payload: axiosInstance.get('/v1/tracks/')
    })
  }
}

export function loadLessons() {
  return function(dispatch) {
    return dispatch({
      type: 'LOAD_LESSONS',
      payload: axiosInstance.get('/v1/lessons/')
    })
  }
}

export function loadExercises() {
  return function(dispatch) {
    return dispatch({
      type: 'LOAD_EXERCISES',
      payload: axiosInstance.get('/v1/exercises/')
    })
  }
}

export function resetNewlyCreatedLessonId() {
  return {
    type: 'RESET_NEWLY_CREATED_EXERCISE_ID'
  }
}
