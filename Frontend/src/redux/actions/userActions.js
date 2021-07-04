// Create Redux action types
export const SET_USERID = 'SET_USERID'
export const SET_USERNAME = 'SET_USERNAME'
export const SET_IS_IN_CALL= 'SET_IS_IN_CALL'

//SETTERS
export const setUserId = (userId) => ({
    type: SET_USERID,
    payload: userId,
})

export const setUsername = (username) => ({
    type: SET_USERNAME,
    payload: username,
})

export const setIsInCall = (isInCall) => ({
    type: SET_IS_IN_CALL,
    payload: isInCall,
})

