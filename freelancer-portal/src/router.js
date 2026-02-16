import { createBrowserRouter } from 'react-router-dom';
import App from './App';
import SignIn from './components/Auth/SignIn';
import SignUp from './components/Auth/SignUp';
import Welcome from './components/Welcome/Welcome';

export const router = createBrowserRouter([
    {
        path: "/",
        element: <App />,
        children: [
            {
                path: "signin",
                element: <SignIn />
            },
            {
                path: "signup",
                element: <SignUp />
            },
            {
                path: "welcome",
                element: <Welcome />
            }
        ]
    }
]);