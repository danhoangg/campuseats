import React, { useState, useEffect } from 'react';
import { useAuth0 } from '@auth0/auth0-react';

const Profile = () => {
    const { getIdTokenClaims } = useAuth0();
    const [idToken, setIdToken] = useState('');
    const [user, setUser] = useState('');
    const [fetchedData, setFetchedData] = useState({})

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
        if (idToken == '') return;
        fetch(`http://lissan.dev:8050/give-me-email?jwt=${idToken}`)
            .then(data => data.json())
            .then(data => setUser(data.email))
    }, [idToken])

    useEffect(() => {
        if (user == '') return;
        fetch(`http://lissan.dev:8050/get-user-info?email=${user}`)
            .then(res => res.json())
            .then(data => setFetchedData(data.users))
    }, [user])

    const [data, setData] = useState({})

    useEffect(() => { 
        setData(fetchedData)
    }, [fetchedData])

    const handleTextChange = (e) => {
        if (e.target.value.length == 20) return;
        setData({ ...data, [e.target.id]: e.target.value })
    }

    const handleNumChange = (e) => {
        if (!/^\d+$/.test(e.target.value)) return;
        setData({ ...data, [e.target.id]: e.target.value })
    }

    const handleBioChange = (e) => {
        if (e.target.value.length == 40) return;
        setData({ ...data, [e.target.id]: e.target.value })
    }

    const handleSubmit = () => {
        fetch(`http://lissan.dev:8050/update-user-info`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({...data, email: user})
        })
        .then(res => {
            if (res.status == 403) {
                setError('Only student accounts allowed, .ac.uk emails')
            }
        })
    }
    
    const [img, setImg] = useState(null)
    const [error, setError] = useState('')

    const handleImgUpload = (e) => {
        const formData = new FormData();
        formData.append('file', img);
        fetch(`http://lissan.dev:8050/upload-pfp?email=${user}`, {
            method: 'POST',
            body: formData
        })
    }

    const handleImgSelect = (e) => {
        setImg(e.target.files[0])
    }    

    return (
        <div className='flex justify-center items-center' style={{ height: `calc(100vh - 4rem)` }}>
            <div className='flex flex-col md:flex-row items-center space-y-4 md:space-y-0 md:space-x-4'>
                <div>
                    <img src={`http://lissan.dev:8050/media/${data.pfp}`} alt="pfp" className='w-80 h-80 object-cover rounded-2xl' />
                    <input className='my-10' type="file" name='filename' accept='image/png, image/jpg, image/jpeg' onChange={handleImgSelect} />
                    <br />
                    <button className='bg-red-400 text-white rounded-lg px-4 py-2' onClick={handleImgUpload}>Upload</button>
                </div>
                <div className='text-center md:text-left'>
                    <div className='flex flex-col items-center md:items-start'>
                        {/* Each row is a flex container */}
                        <div className='flex items-center my-5'>
                            <p className='text-right w-24 text-2xl'>Name:</p>
                            <input id='name' type="text" value={data.name} className="ml-2" onChange={handleTextChange} />
                        </div>
                        <div className='flex items-center my-5'>
                            <p className='text-right w-24 text-2xl'>Gender:</p>
                            <select id='gender' value={data.gender} className="ml-2" onChange={handleTextChange}>
                                <option value="Male">Male</option>
                                <option value="Female">Female</option>
                            </select>
                        </div>
                        <div className='flex items-center my-5'>
                            <p className='text-right w-24 text-2xl'>Year:</p>
                            <input id='year' type="text" value={data.year} className="ml-2" onChange={handleNumChange} />
                        </div>
                        <div className='flex items-center my-5'>
                            <p className='text-right w-24 text-2xl'>Course:</p>
                            <input id='course' type="text" value={data.course} className="ml-2" onChange={handleTextChange} />
                        </div>
                        <div className='flex items-center my-5'>
                            <p className='text-right w-24 text-2xl'>Bio:</p>
                            <textarea id='bio' type="text" value={data.bio} className="ml-2 resize h-32 w-96" onChange={handleBioChange}/>
                        </div>
                        <div>
                            <button className='bg-red-400 text-white rounded-lg px-4 py-2 my-4' onClick={handleSubmit}>Save</button>
                            <p>{error}</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Profile;
