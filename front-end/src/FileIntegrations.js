import React from 'react'

const FileIntegrations = () => {
    const data = [{
        title: 'File Integrations:',
        content: 'Index.js',
      },
      {
        title: 'External API Connections:',
        content: 'https://pokemonapi.com/api/v/1.1                [line 12]',
      },
      {
        title: 'Internal API Endpoints:',
        content: '/home               [HTTP GET]',
      },
      
    ]
  return (
    <div className='border- border-2 border-sky-500 w-fit h-3/4'>
        {data.map((data , _i) => (
            <div>
                <h4 className='text-white'>{data.title}</h4>
                <h3 className='font-bold text-amber-400'>{data.content}</h3>
            </div>
            
        ))}
    </div>
  )
}

export default FileIntegrations