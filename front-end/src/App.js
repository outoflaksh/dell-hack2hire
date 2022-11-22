import logo from './logo.svg';
import './App.css';
import fish from './FishSkeleton.png'
import TechStack from './TechStack';
import CodeBase from './CodeBase';
import FileIntegrations from './FileIntegrations';
import ExternalLib from './ExternalLib';
import OutdatedDependencies from './OutdatedDependencies';
function App() {
  return (
    <div className="App">
      
        <div className='bg-[#404258] h-full w-full '>
          <div>
            <img src = {fish} className = "object-center content-center"></img>
            <h2 className = "text-white">Skeleton</h2>
          </div>
          
          <TechStack></TechStack>
          <CodeBase></CodeBase>
          <FileIntegrations></FileIntegrations>
          <ExternalLib></ExternalLib>
          <OutdatedDependencies></OutdatedDependencies>
        </div>
      
    </div>
  );
}

export default App;
