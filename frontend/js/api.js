/**
 * TAXTABOZOR81 API Client
 * Backend Django REST Framework bilan to'liq asinxron muloqot
 */

const API_CONFIG = {
  BASE_URL: (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')
    ? 'http://127.0.0.1:8000/api'
    : '/api',
  TIMEOUT: 10000,
};

class ApiError extends Error {
  constructor(message, status, data) {
    super(message);
    this.status = status;
    this.data = data;
  }
}

async function request(endpoint, options = {}) {
  const url = `${API_CONFIG.BASE_URL}/${endpoint.replace(/^\//, '')}`;
  const headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    ...(options.headers || {}),
  };

  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), API_CONFIG.TIMEOUT);

    const response = await fetch(url, {
      ...options,
      headers,
      signal: controller.signal,
    });
    clearTimeout(timeoutId);

    if (!response.ok) {
      let errorData;
      try {
        errorData = await response.json();
      } catch {
        errorData = { detail: response.statusText };
      }
      throw new ApiError(errorData.detail || errorData.error || 'Serverda xatolik', response.status, errorData);
    }

    if (response.status === 204) return null;
    return await response.json();
  } catch (err) {
    console.error(`[API Error] ${endpoint}:`, err);
    throw err;
  }
}

window.API = {
  // --- Catalog & Products ---
  async getCategories() {
    return request('products/categories/');
  },

  async getProducts(params = {}) {
    const query = new URLSearchParams();
    if (params.category) query.append('category', params.category);
    if (params.search) query.append('search', params.search);
    if (params.min_price) query.append('min_price', params.min_price);
    if (params.max_price) query.append('max_price', params.max_price);

    const queryString = query.toString();
    return request(`products/${queryString ? `?${queryString}` : ''}`);
  },

  async getProductDetail(id) {
    return request(`products/${id}/`);
  },

  // --- Users & Profile ---
  async getUser(telegramId) {
    return request(`users/me/?telegram_id=${telegramId}`);
  },

  async registerUser(userData) {
    return request('users/register/', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
  },

  async updateUser(telegramId, data) {
    return request(`users/me/?telegram_id=${telegramId}`, {
      method: 'PATCH',
      body: JSON.stringify(data),
    });
  },

  // --- Addresses ---
  async getAddresses(telegramId) {
    return request(`users/addresses/?telegram_id=${telegramId}`);
  },

  async addAddress(telegramId, addressData) {
    return request(`users/addresses/?telegram_id=${telegramId}`, {
      method: 'POST',
      body: JSON.stringify(addressData),
    });
  },

  async deleteAddress(addressId) {
    return request(`users/addresses/${addressId}/`, {
      method: 'DELETE',
    });
  },

  // --- Cart ---
  async getCart(telegramId) {
    return request(`cart/?telegram_id=${telegramId}`);
  },

  async addToCart(telegramId, productId, quantity = 1) {
    return request('cart/add/', {
      method: 'POST',
      body: JSON.stringify({
        telegram_id: telegramId,
        product_id: productId,
        quantity: quantity,
      }),
    });
  },

  async removeFromCart(telegramId, productId) {
    return request('cart/remove/', {
      method: 'POST',
      body: JSON.stringify({
        telegram_id: telegramId,
        product_id: productId,
      }),
    });
  },

  async clearCart(telegramId) {
    return request('cart/clear/', {
      method: 'POST',
      body: JSON.stringify({
        telegram_id: telegramId,
      }),
    });
  },

  // --- Orders ---
  async createOrder(telegramId, addressId, paymentMethod = 'cash', comment = '') {
    return request('orders/create/', {
      method: 'POST',
      body: JSON.stringify({
        telegram_id: telegramId,
        address_id: addressId,
        payment_method: paymentMethod,
        comment: comment,
      }),
    });
  },

  async getOrders(telegramId) {
    return request(`orders/?telegram_id=${telegramId}`);
  },

  async getOrderDetail(orderId) {
    return request(`orders/${orderId}/`);
  },
};
