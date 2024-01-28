import React from 'react';

const Contact = (props) => {

    const handleClick = () => {
        props.onSelect(props.id)
    }

    const contactStyle = {
        backgroundColor: props.selected ? 'rgb(180 180 180)' : 'transparent'
    };

    return (
        <div className='flex items-center border-b-2 border-b-white py-4 px-3 hover:cursor-pointer' style={contactStyle} onClick={handleClick}>
            <img src={props.pfp} alt="pfp" className='h-10 w-10 mr-2 rounded-full'/>
            <p className='text-2xl ml-3'>{props.name}</p>
        </div>
    )
}

export default Contact;


