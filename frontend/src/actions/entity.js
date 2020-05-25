import axiosInstance from "../axiosApi"

async function performExerciseLoading(id) {
  const response = await axiosInstance.get(`/v1/exercises/${id}/`)
  return response?.data
}

async function performExerciseSaving(id, data) {
  const response = await axiosInstance.put(`/v1/exercises/${id}/`, data)
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

function failedToSave(error) {
  return {
    type: 'FAILED_TO_SAVE',
    payload: error
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
    })
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
