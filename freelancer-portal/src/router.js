// import { createBrowserRouter } from 'react-router-dom';
// import App from './App';
// import SignIn from './components/Auth/SignIn';
// import SignUp from './components/Auth/SignUp';
// import Welcome from './components/Welcome/Welcome';

// export const router = createBrowserRouter([
//     {
//         path: "/",
//         element: <App />,
//         children: [
//             {
//                 path: "signin",
//                 element: <SignIn />
//             },
//             {
//                 path: "signup",
//                 element: <SignUp />
//             },
//             {
//                 path: "welcome",
//                 element: <Welcome />
//             }
//         ]
//     }
// ]);
// src/router.js
import { createBrowserRouter } from 'react-router-dom';
import App from './App';
import SignIn from './components/Auth/SignIn';
import SignUp from './components/Auth/SignUp';
import Welcome from './components/Welcome/Welcome';
import Notifications from './pages/Notifications'; // Add this import
import VerifyEmail from './pages/VerifyEmail'; // Add this import

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
            },
            {
                path: "notifications", // Add notifications route
                element: <Notifications />
            },
            {
                path: "verify-email",
                element: <VerifyEmail />
            },
            {
                path: "verify-email/:token",
                element: <VerifyEmail />
            }
        ]
    }
]);