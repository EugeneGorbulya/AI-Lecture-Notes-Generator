export const saveToken = (token) => {
  localStorage.setItem('access_token', token);
};

export const getToken = () => {
  return localStorage.getItem('access_token');
};

export const saveUserId = (id) => {
  localStorage.setItem('user_id', id);
};

export const getUserId = () => {
  return localStorage.getItem('user_id');
};

export const clearAuth = () => {
  localStorage.removeItem('access_token');
  localStorage.removeItem('user_id');
};
