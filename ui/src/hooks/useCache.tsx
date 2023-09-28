import { Dispatch, createContext, useContext, useReducer } from "react";

type CacheState = {
  searches: { [searchId: string]: object[] };
};

type CacheAction = {
  type: "SET_SEARCH";
  payload: { searchId: string; videos: object[] };
};

const initialState: CacheState = {
  searches: {},
};

const reducer = (state: CacheState, action: CacheAction): CacheState => {
  switch (action.type) {
    case "SET_SEARCH":
      const { searches, ...rest } = state;
      searches[action.payload.searchId] = action.payload.videos;
      return { searches, ...rest };
    default:
      return state;
  }
};

export const CacheContext = createContext<{ state: CacheState; dispatch?: Dispatch<CacheAction> }>({ state: initialState });

export const CacheProvider = ({ children }: { children: JSX.Element }) => {
  const [state, dispatch] = useReducer(reducer, initialState);
  const value = { state, dispatch };
  return <CacheContext.Provider value={value}>{children}</CacheContext.Provider>;
};

export const useCache = () => {
  const { state, dispatch } = useContext(CacheContext);
  return {
    getVideosBySearchId: (searchId: string) => {
      return state.searches[searchId];
    },
    setVideosBySearchId: (searchId: string, videos: object[]) => {
      dispatch!({ type: "SET_SEARCH", payload: { searchId, videos } });
    },
  };
};
