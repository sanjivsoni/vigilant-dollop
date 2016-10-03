Rails.application.routes.draw do
  devise_for :users
	root 'static_pages_controller#home' 
end
