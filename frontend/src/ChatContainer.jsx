import React, {useEffect, useState, useRef} from 'react';
import Contact from './Contact';
import Message from './Message';
import { useAuth0 } from '@auth0/auth0-react';

import { SlArrowLeft, SlArrowRight } from "react-icons/sl";
import './index.css';


const ChatContainer = () => {
    const { getIdTokenClaims } = useAuth0();
    const [idToken, setIdToken] = useState('');
    const [user, setUser] = useState('');

    useEffect(() => {
        const fetchIdToken = async () => {
            try {
                const idTokenClaims = await getIdTokenClaims();
                setIdToken(idTokenClaims.__raw);
            } catch (error) {
                console.error('Error getting ID token', error);
            }
        };

        fetchIdToken();
    }, [getIdTokenClaims]);

    useEffect(() => {
        fetch(`https://backend.unimatch.lissan.dev/give-me-email?jwt=${idToken}`)
            .then(res => res.json())
            .then(res => setUser(res.email))
    }, [idToken])
    
    const [selected, setSelected] = useState(null);
    const [messages, setMessages] = useState([])
    const [currentMessage, setCurrentMessage] = useState('')
    const [contacts, setContacts] = useState([])
    const [trigger, setTrigger] = useState(false)

    useEffect(() => {
        if (user == '') return;
        fetch(`https://backend.unimatch.lissan.dev/contact-list?user=${user}`)
            .then(res => res.json())
            .then(data => setContacts(data.contact_list))
    }, [user])

    useEffect(() => {
        if (selected == null || user == '') return;
        let receiver = contacts[selected][0]
        fetch(`https://backend.unimatch.lissan.dev/messages?user=${user}&other=${receiver}`)
            .then(res => res.json())
            .then(data => setMessages(data.messages))
    }, [selected, user, trigger])

    useEffect(() => {
        const interval = setInterval(() => {
            setTrigger(prevTrigger => !prevTrigger)
        }, 1000);

        return () => {
            clearInterval(interval);
        };
    }, []);

    const endOfListRef = useRef(null);
    const scrollToBottom = () => {
        endOfListRef.current?.scrollIntoView();
    };
    useEffect(scrollToBottom, [messages]);

    const handleSelect = (id) => {
        setSelected(id);
    }

    const handleChange = (e) => {
        setCurrentMessage(e.target.value)
    }
    
    const keyDown = (e) => {
        if (selected == null) return;
        if (e.key == "Enter") {
            let receiver = contacts[selected][0]
            fetch(`https://backend.unimatch.lissan.dev/send-message?user=${user}&other=${receiver}&message=${currentMessage}`)
            setCurrentMessage('')
        }
    }
    
    const [isContactsVisible, setIsContactsVisible] = useState(true);

    const toggleContacts = () => {
        setIsContactsVisible(!isContactsVisible);
    };

    return (
        <div className="flex mx-auto relative" style={{ height: `calc(100vh - 4rem)` }}>
            <div className={`${isContactsVisible ? 'md:w-1/4 w-screen' : 'hidden'}  bg-gray-200 overflow-y-auto`}>
            {contacts.length > 0 && (
                    contacts.map((contact, i) => {
                        return <Contact id={i} key={i} email={contact[0]} selected={selected === i} onSelect={handleSelect} name={contact[1]} pfp={"https://backend.unimatch.lissan.dev/media/" + contact[2]} />
                    })
                )}
            </div>

            <div className={`flex items-center`} style={{ height: `calc(100vh - 4rem)` }}>
                <button 
                    onClick={toggleContacts}
                    className={`bg-gray-600 text-white p-3 rounded-full shadow-lg ${isContactsVisible ? '-translate-x-12' : 'translate-x-2'} absolute`}
                    style={{ zIndex: 10 }}
                >
                    {isContactsVisible ? <SlArrowLeft /> : <SlArrowRight />}
                </button>
            </div>

            <div className={`${isContactsVisible ? 'md:w-3/4 hidden' : 'w-full flex'} bg-white px-4 pb-4 flex-col md:flex`}>
                <div className="overflow-y-auto flex-grow">
                    {messages.map((m, i) => (
                        <Message key={i} text={m[1]} sender={m[2]} time={m[0]}/>
                    ))}
                    <div ref={endOfListRef} />
                </div>

                <div className="mt-4">
                    <input 
                        type="text" 
                        className="border p-2 w-full" 
                        placeholder="Type a message..." 
                        value={currentMessage} 
                        onChange={handleChange} 
                        onKeyDown={keyDown}
                    />
                </div>
            </div>
        </div>
    );
};


export default ChatContainer;