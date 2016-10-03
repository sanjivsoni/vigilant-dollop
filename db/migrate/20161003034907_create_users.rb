class CreateUsers < ActiveRecord::Migration
  def change
    create_table :users do |t|
      t.string :userid
      t.string :name
      t.string :password
      t.string :email
      t.string :mobile
      t.string :dob
      t.string :ssn
      t.integer :ssntype
      t.string :address
      t.string :pincode
      t.string :secondarypwd

      t.timestamps null: false
    end
  end
end
