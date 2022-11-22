import React from 'react'

const ExternalLib = () => {
    const data = [{
        title: 'External Libraries',
        content: 'express v18.0.2',
      },
      
      ]
  return (
    <div className='mt border- border-2 border-sky-500 w-fit h-3/4'>
        {data.map((data , _i) => (
            <div>
                <h4 className='text-white'>{data.title}</h4>
                <h3 className='font-bold text-amber-400'>{data.content}</h3>
            </div>
            
        ))}
    </div>
  )
}

export default ExternalLib