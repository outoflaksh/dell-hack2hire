import React from 'react'

const CodeBase = () => {
    const data = [{
        title: 'Scanned Codebase:',
        content: 'sample-express-codebase',
      },
      {
        title: 'Number of Scanned Files',
        content: '2',
      },]
  return (
    <div className=' border- border-2 border-sky-500 w-fit h-3/4'>
        {data.map((data , _i) => (
            <div>
                <h4 className='text-white'>{data.title}</h4>
                <h3 className='font-bold text-amber-400'>{data.content}</h3>
            </div>
            
        ))}
    </div>
  )
}

export default CodeBase