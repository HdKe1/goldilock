import { Link, useLocation } from 'react-router-dom';
import { ACCESS_TOKEN } from '../constants';

function Navbar() {
  const location = useLocation(); 
  const isAuthenticated = localStorage.getItem(ACCESS_TOKEN);

  return (
    <nav className="bg-blue-900 px-6 py-4">
      <div className="flex justify-between items-center">
        <Link to="/" className="text-white text-xl font-semibold hover:text-blue-200 transition-colors">
          goldilock
        </Link>
        <div className="flex space-x-4">
          {isAuthenticated ? (
            <>
              <Link 
                to="/results" 
                className="text-white px-4 py-2 rounded hover:bg-blue-800 transition-colors"
              >
                Results
              </Link>
              <Link 
                to="/logout" 
                className="text-white px-4 py-2 rounded hover:bg-blue-800 transition-colors"
              >
                Logout
              </Link>
            </>
          ) : (
            <>
              <Link 
                to="/login" 
                className="text-white px-4 py-2 rounded hover:bg-blue-800 transition-colors"
              >
                Login
              </Link>
              <Link 
                to="/register" 
                className="text-white px-4 py-2 rounded hover:bg-blue-800 transition-colors"
              >
                Register
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  )
}

export default Navbar