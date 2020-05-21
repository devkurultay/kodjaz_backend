import axiosInstance from "../axiosApi"

async function performExerciseLoading(id) {
  const response = await axiosInstance.get(`/v1/exercises/${id}/`)
  return response?.data
}

function getExercise(response) {
  return {
    type: 'LOAD_EXERCISE',
    payload: response
  }
}

export function loadExercise(id) {
  return function (dispatch) {
    return performExerciseLoading(id).then(
      (response) => dispatch(getExercise(response)),
      (error) => dispatch(failToLogIn(error))
    )
  }
}
