// Create Redux action types
export const SET_UP = 'SET_UP'
export const START = 'START'
export const SET_MOUNTED = 'MOUNTED'
export const SET_STATE = 'SET_STATE'
export const SET_SESSION='SET_SESSION'
export const SET_INCOMING_SESSION='SET_INCOMING_SESSION'
export const CALL = 'CALL'
export const HANGUP= 'HANGUP'
export const PICKUP='PICKUP'

//SETTERS
export const setUpPhone = (userId) => ({
    type: SET_UP,
    payload:userId
})
//SETTERS
export const startPhone = (ua) => ({
    type: START,
    payload:ua
})

export const setPhoneState = (state) => ({
    type: SET_STATE,
    payload: state
})

export const setPhoneSession = (session) => ({
    type: SET_SESSION,
    payload: session
})
export const setPhoneIncomingSession = (incSession) => ({
    type: SET_INCOMING_SESSION,
    payload: incSession
})
export const call = (user) => ({
    type: CALL,
    payload:user
})

export const hangUpPhone = () => ({
    type: HANGUP,
})

export const pickUpPhone = () => ({
    type: PICKUP,
})
