import React from 'react'

const Alert = (props) => {
  return (
    <div style={{height:'60px'}}>
    { props.alert && <div class={`alert alert-${props.alert.type} alert-dismissible fade show`}role="alert">
   {props.alert.msg}
   
 </div>}
 </div>
  )
}

export default Alert