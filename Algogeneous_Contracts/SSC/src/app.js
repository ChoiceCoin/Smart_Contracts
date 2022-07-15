import { Suspense } from "react";


import { Provider as ReduxProvider } from "react-redux";
import { BrowserRouter as Router } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "react-query";

import AlertModal from "./statics/alertmodal";
import WalletConfirmation from "./statics/walletConfirmation";
import FormAlert from "./statics/formalert";
import mainpage from "./mainpage";
import stores from "./store/stores";

const renderLoader = () => <p></p>;

const App = () => {
  const queryClient = new QueryClient();
  return (
    <Suspense fallback={renderLoader()}>
      <ReduxProvider store={stores}>
        <QueryClientProvider client={queryClient}>
          <Router>
            <MainPage />
            <WalletConfirmation />
            <FormAlert/>
            <AlertModal />
          </Router>
        </QueryClientProvider>
      </ReduxProvider>
    </Suspense>
  );
};

export default App;
