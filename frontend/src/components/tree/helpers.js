export const dataToTree = (data) => {
  return data.map(track => {
    return {
      id: track.id,
      title: track.name,
      subtitle: track.description,
      expanded: false,
      name: track.name,
      description: track.description,
      is_published: track.is_published,
      programming_language: track.programming_language,
      type: track.entity_type,
      childrenType: 'Unit',
      children: getUnits(track.track_units)
    }
  })
}

const getUnits = (units) => {
  return units.map(unit => {
    return {
      id: unit.id,
      title: unit.name,
      subtitle: unit.description,
      is_published: unit.is_published,
      track: unit.track,
      expanded: true,
      type: unit.entity_type,
      childrenType: 'Lesson',
      children: getLessons(unit.unit_lessons)
    }
  })
}

const getLessons = (lessons) => {
  return lessons.map(lesson => {
    return {
      id: lesson.id,
      title: lesson.name,
      is_published: lesson.is_published,
      unit: lesson.unit,
      is_published: lesson.is_published,
      unit: lesson.unit,
      expanded: true,
      type: lesson.entity_type,
      childrenType: 'Exercise',
      children: getExercises(lesson.lesson_exercises)
    }
  })
}

const getExercises = (exercises) => {
  return exercises.map(exercise => {
    return {
      id: exercise.id,
      title: exercise.name.slice(0,12) + "...",
      type: exercise.entity_type,
      childrenType: null,
    }
  })
}
