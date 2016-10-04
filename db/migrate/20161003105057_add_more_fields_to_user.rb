class AddMoreFieldsToUser < ActiveRecord::Migration
  def change
	  add_column :users, :name, :string
	  add_column :users, :mobile, :string
	  add_column :users, :dob, :string
	  add_column :users, :ssn, :string
	  add_column :users, :ssntype, :string
	  add_column :users, :address, :string
	  add_column :users, :pincode, :string
	  add_column :users, :secondarypwd, :string
  end
end
